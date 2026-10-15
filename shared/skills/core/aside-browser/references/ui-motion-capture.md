# Screenshot-led UI motion capture

Use when a user wants a product explained control by control, including hover behavior, transitions and animation. This recipe handles browser evidence and media; walkthrough order and captions follow the project's QA procedure.

## 1. Prepare the next interaction

1. Use the already verified, owned Aside page in its persistent REPL. Resolve the output directory with `path.resolve()` and create only the capture folders needed for the current interaction.
2. Inspect a fresh snapshot, then the visible control's DOM attributes and `getBoundingClientRect()`. Select an observed ref or CSS locator. When a name lookup fails, inspect the actual rendered label and element before using a native mouse click at its measured center.
3. Capture the settled starting state as a full PNG. Inspect a hover state separately. Move the pointer away for neutral screenshots, because a retained hover can resemble another selected navigation item.
4. Install bounded page-local observation before the action. Listen for `transitionrun`, `transitionend`, `animationstart` and `animationend`; record the event target, property/name, `elapsedTime` and `performance.now()`. Read target classes with `getAttribute('class')`, because SVG `className` is an object and can lose its value during JSON serialization. For asynchronous answers, also follow `live-progress-observation.md` to retain distinct visible-text states.

## 2. Sample actual motion

- Capture before the action and several frames immediately afterward in one REPL submission. For fast onset, use the inspected control's center with `page.mouse.click()`; higher-level locator actions can return after part of the transition has passed.
- Save actual capture timestamps. Screenshot acquisition and bridge overhead add to the requested delay, so a sleep interval alone does not establish the frame rate.
- Inspect `document.getAnimations()` during sampling when useful. Record `animationName`, `effect.target`, `effect.getTiming()` and visible geometry. Attribute a motion claim to the product element being inspected; keep unrelated overlays and pointer effects out of that claim.
- For end-state layout checks, wait for the observed finite transition to finish and take a separate settled screenshot. Check timing finiteness in the page before serializing it, because infinite iteration counts can become `null` in JSON. Keep repeating indicators outside this wait.
- If sampling misses a short transition, retain the observed CSS/animation timing separately from the pixel evidence. Repeat a safe presentation-only interaction when needed; reopen an accepted result instead of submitting another provider job solely to improve a recording.

Example sampler after `ui` has been bound to the verified owned page:

```javascript
var frames = [];
var captureFrame = async function (name) {
  var started = Date.now();
  await ui.screenshot({path: './artifacts/evidence/frames/' + name});
  frames.push({file: name, startedAt: started, completedAt: Date.now()});
};
await fs.mkdir('./artifacts/evidence/frames', {recursive: true});
await captureFrame('control_00.png');
// Run the inspected native control action here, once.
for (var i = 1; i <= 9; i++) {
  await captureFrame('control_' + String(i).padStart(2, '0') + '.png');
  await sleep(40);
}
await fs.writeFile('./artifacts/evidence/frames/manifest.json',
  JSON.stringify(frames, null, 2));
```

Derive animation duration from observed transition events or animation timing. Describe a computed CSS duration as a declared duration when completion was not observed. Treat screenshot timestamps as sampling times; they can span a different interval from the product's animation.

## 3. Crop and encode locally

1. Preserve the full PNGs. Convert inspected CSS coordinates to image pixels using the actual PNG dimensions and measured CSS viewport dimensions; apply the full-image crop rule in `SKILL.md`.
2. Use Pillow to crop and resize the real frames consistently. Keep the same crop across a transition so movement remains visible in context.
3. Build GIF frame durations from successive capture timestamps rather than assigning a synthetic fixed FPS. Optional pauses on the first and final frames help the reviewer see the states; retain the original manifest so those presentation pauses remain distinct from measured product timing.
4. Encode with Pillow's `save_all=True`, `append_images`, `duration`, `loop=0` and `disposal=2`. Use the existing Python environment when Pillow is available, or an isolated `uv run --no-project --with pillow` invocation for the media script.
5. Decode every frame of the encoded GIF with `Image.open()`, `seek()` and `load()`. Inspect an intermediate and final frame as pixels. Read `n_frames` from the output when reporting a total, because encoding can merge identical source frames.
6. Label widely separated saved-state captures as a step sequence or timelapse. Preserve actual samples for motion evidence; interpolation or reconstructed UI would change what was observed.

## 4. Deliver and stop cleanly

- Place numbered final screenshots and GIFs in one reviewer-facing folder; store raw frames, manifests and timing logs under `evidence/`.
- Attach a full view for orientation, focused before/after views for each control, and a GIF when movement matters. Describe action → visible change → available next action beside the media.
- State the inspected interaction coverage explicitly. A screenshot of an option proves its presentation; executing it and reading back its effect establishes behavior.
- Disconnect observers and remove the event handlers when the recording scope ends. Preserve saved receipts and user-owned tabs during cleanup.
- When the user requests the collected folder, hand over that existing directory and pause the tour. Keep further capture work scoped to a renewed request.
