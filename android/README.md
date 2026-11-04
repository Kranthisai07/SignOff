# Glasses capture: a patch to Meta's CameraAccess sample

**Status (Nov 3, from the user's screenshots):** the patched sample builds and runs on a Galaxy S25 Ultra, connects to Ray-Ban Meta Gen 2, and shows the live glasses camera feed ("Session: started, Stream: streaming"). The laptop server is tested (`python -m eval.test_selfcheck`). **Round trip confirmed (Nov 3, 10:02 PM):** a photo captured through the glasses, sent with the S1 button, came back as a verdict in the app (`UNSURE`, "No pan is visible in the photo, only a laptop, phone, and couch", latency 7.3 s), and the frame plus a log line landed in `runs/live/`. Not yet tried on a real egg step.

Meta's sample app is not copied into this repo (it falls under the Meta Wearables Developer Terms). This folder holds only our change, `signoff-glasses.patch`, made against [facebook/meta-wearables-dat-android](https://github.com/facebook/meta-wearables-dat-android) release 1.0.1 (commit `f4371bc9f90249d51eb07d7f8a61e8d829294f16`). Verified: the patch applies cleanly to a pristine checkout of that commit.

**What the patch does:** after you capture a photo through the glasses, the preview screen shows buttons S1 to S5. Tapping one sends the photo (resized to 1288 px, JPEG) to a local Signoff server and shows the verdict and reason. Files touched: `app/build.gradle.kts` (a `SIGNOFF_URL` build field), `AndroidManifest.xml` (cleartext HTTP, for the local server only), `CapturePreviewScreen.kt` (buttons and result text), and a new `SignoffClient.kt`.

## Run it
1. **Glasses:** per Meta's Version Dependencies page (read Nov 3), SDK 1.0.1 needs Meta AI app V292 and glasses firmware V128; SDK 1.0.0 needs V290 and V128. The sample is pinned to SDK 1.0.1, so update the Meta AI app and glasses firmware first. In the Meta AI app: Settings, App Info, tap the app version 5 times, switch Developer Mode on and confirm.
2. **Phone:** Settings, About phone, Software information, tap Build number 7 times; then Developer options, USB debugging on. Connect by USB and accept the prompt. `adb devices` should list the phone.
3. **App:**
   ```
   git clone https://github.com/facebook/meta-wearables-dat-android.git D:\signoff-dat
   cd D:\signoff-dat
   git checkout f4371bc9f90249d51eb07d7f8a61e8d829294f16
   git apply D:\SignOff\android\signoff-glasses.patch
   ```
   Create `samples\CameraAccess\local.properties` with `mwdat_application_id=0` and `mwdat_client_token=0` (Developer Mode needs no real IDs). Open `samples\CameraAccess` in Android Studio (Narwhal 2025.1.1 or newer, JDK 17), let it sync and install SDK 36 if asked, then Run on the phone.
4. **Server (laptop):**
   ```
   cd D:\SignOff
   python -m signoff.server
   adb reverse tcp:8000 tcp:8000
   ```
   The server binds to 127.0.0.1 only. The phone reaches it through the USB reverse tunnel, so the Meta API key stays on the laptop.
5. **In the app:** Connect, Start Session, Preview, capture a photo, then tap S1 to S5.

Every frame and verdict is saved under `runs/live/` (gitignored) with a `log.jsonl` audit trail.

## Limits
- Photo capture only (the sample's own capture button), not continuous video. Latency is the model call, about 4 s median in the benchmark.
- No authentication on the local server; it listens on loopback only.
- Requires the phone connected by USB for the tunnel.
