"""Extract still frames from a video with ffmpeg."""
import subprocess
from pathlib import Path


def extract(video, t_start: float, t_end: float, n: int, out_dir, stem: str) -> list[Path]:
    """n frames evenly spaced inside [t_start, t_end] seconds, width capped at 1288 px."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for i in range(n):
        t = t_start + (t_end - t_start) * (i + 1) / (n + 1)
        p = out_dir / f"{stem}_f{i + 1}.jpg"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(video),
             "-frames:v", "1", "-vf", "scale='min(1288,iw)':-2", "-q:v", "3", str(p)],
            check=True,
        )
        paths.append(p)
    return paths
