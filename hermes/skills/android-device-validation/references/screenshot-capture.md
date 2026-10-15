# Android screenshot capture

## Binary-safe ADB capture

Run ADB through a byte-returning subprocess and save screenshots under the configured scratch directory. On multi-display devices, `screencap` can prepend a textual display warning to stdout even when capture succeeds. Extract the payload at the PNG signature before passing it to an image viewer; the prefix makes an otherwise valid capture unrecognizable.

```python
from pathlib import Path
import subprocess

raw = subprocess.check_output(
    ['adb', '-s', serial, 'exec-out', 'screencap', '-p'],
    timeout=20,
)
signature = b'\x89PNG\r\n\x1a\n'
start = raw.find(signature)
if start < 0:
    raise RuntimeError('Capture returned no PNG payload')
output = Path(scratch_directory) / 'device-screen.png'
output.write_bytes(raw[start:])
```

Load the saved image with the available image-inspection tool. If an image library is available, decode or verify the PNG as an additional format check; keep visual inspection as the feature-verification gate.

## Foldable display and coordinates

1. Inspect the capture dimensions and content before tapping. Folded and unfolded states can change both viewport size and visible controls.
2. Account for any downscaling reported by the image tool: convert displayed coordinates back to original-image pixels before sending `adb shell input tap`.
3. If the capture shows an unexpected display, inspect `adb -s "$SERIAL" shell dumpsys display` and the screenshot command's supported display-selection flags. Select the active display using discovered identifiers.
4. Re-capture after opening selectors, changing modes, or scrolling. Native selectors and sticky panels change available hit targets.
5. Treat an empty UIAutomator text extraction as a reason to inspect the screenshot; WebView-rendered content may supply limited accessibility text while remaining fully visible.

## Visible-result check

Verify the feature label, current selection, changed controls, and relevant output in the screenshot. Leave the app in a stopped, inspectable state when handing it back. An installation timestamp supports installation verification; the final rendered feature supports user-flow verification.
