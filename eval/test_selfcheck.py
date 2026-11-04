"""No-API self-check: python -m eval.test_selfcheck"""
import subprocess
import tempfile
from pathlib import Path

from eval.run import score, wilson
from signoff import frames
from signoff.verifier import combine

# combine: biased against false passes
assert combine(["pass", "pass", "pass"]) == "pass"
assert combine(["pass", "fail", "pass"]) == "fail"
assert combine(["pass", "unsure"]) == "unsure"
assert combine(["pass", "invalid"]) == "unsure"
assert combine([]) == "unsure"

# score: 2 fail rows (1 false pass), 2 pass rows (1 false fail, 1 unsure counted not correct)
rows = [{"truth": "fail", "verdict": "pass"}, {"truth": "fail", "verdict": "fail"},
        {"truth": "pass", "verdict": "fail"}, {"truth": "pass", "verdict": "unsure"}]
s = score(rows)
assert (s["false_pass_rate"]["k"], s["false_pass_rate"]["n"]) == (1, 2)
assert (s["false_fail_rate"]["k"], s["false_fail_rate"]["n"]) == (1, 2)
assert (s["accuracy"]["k"], s["unsure_rate"]["k"]) == (1, 1)
assert score([])["accuracy"]["rate"] is None
lo, hi = wilson(5, 10)
assert 0.23 < lo < 0.24 and 0.76 < hi < 0.77  # known Wilson 95% for 5/10

# frames: 3 frames from a 6 s synthetic video, ffmpeg only
with tempfile.TemporaryDirectory() as d:
    vid = Path(d) / "t.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "testsrc=size=640x480:rate=10",
                    "-t", "6", str(vid)], check=True)
    got = frames.extract(vid, 1.0, 5.0, 3, Path(d) / "f", "x")
    assert len(got) == 3 and all(p.stat().st_size > 1000 for p in got)
# server: input validation answers before any API call (bad step, non-JPEG body)
import http.client
import threading
from http.server import ThreadingHTTPServer

from signoff.server import Handler

srv = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
for path, body in [("/verify?step=9", b"\xff\xd8x"), ("/verify?step=2", b"not a jpeg"), ("/nope", b"x")]:
    c = http.client.HTTPConnection("127.0.0.1", srv.server_port)
    c.request("POST", path, body)
    assert c.getresponse().status in (400, 404), path
srv.shutdown()
print("selfcheck ok")
