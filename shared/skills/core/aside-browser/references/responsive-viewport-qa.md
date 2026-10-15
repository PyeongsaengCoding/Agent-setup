# Responsive viewport QA

## Procedure

1. Read a fresh snapshot of the app and check `typeof qaPage.setViewportSize`. Use native resizing when supported. Otherwise create a separate owned QA tab at the verified local app entry URL; keep the user's existing app tab intact.
2. In the owned tab only, create a same-origin iframe with explicit CSS width and height. Set its `src` to the working entry URL discovered during navigation. Replacing the owned tab's body is an ephemeral QA harness; preserve application files and unrelated tabs.
3. Take a snapshot after frame creation. If the frame is still loading, take another snapshot when it is ready. Dismiss onboarding through fresh frame refs, then select the target mode, key, and form through locator actions.
4. Measure inside the iframe: `contentWindow.innerWidth`, `innerHeight`, and `contentDocument.documentElement.scrollWidth`. Record actual dimensions with the requested dimensions; scrollbar space can reduce the document's layout width.
5. Inspect the desktop and narrow layouts visually. Record menu labels, selected styling, text clipping, button spacing, document overflow, intentional horizontal scrolling, and fixed-header/footer overlap. Keep functional action evidence separate from layout evidence.
6. For a control below the screenshot viewport, use its observed element to scroll the iframe document, then read its bounding rectangle and the scrolling element's scrollTop. Capture again. A successful locator click and changed application state can coexist with an unchanged screenshot because the frame has not visibly scrolled.
7. Exercise meaningful states through real controls, then carry a desktop-created state across the narrow breakpoint instead of testing only a fresh mobile mount. For collapsible sidebars or evidence rails, measure the main content's width and left edge, computed grid tracks, and the rail's computed display and rectangle in both states. Document overflow alone can pass while the main column is compressed or a supposedly hidden rail still consumes a row; inspect winning compound-state selectors for both grid and visibility properties. Read back the expected labels, enabled states, and target range through a fresh snapshot. Claim audible playback only when audio has been independently verified.
8. Save screenshots and measured viewport data together. Immediately before each capture, assert the iframe's actual width/height and the required visible state; derive that capture's manifest fields from those measurements. When a prior action fails, verify these assertions again before assigning a desktop/mobile or open-panel label. Retain mislabeled captures as diagnostic-only and take a fresh same-condition capture for acceptance. Load the images for visual inspection before reporting. For useful crops, derive scale from actual screenshot pixels and the measured capture surface, then crop locally; arbitrary clip offsets or assumed devicePixelRatio can produce misleading crops.
9. After a layout fix, render a representative question, answer and expanded/collapsed history at desktop and narrow widths; an empty-state geometry check does not exercise text wrapping or disclosure height. Capture the same affected states after the final edit and inspect their pixels. Pair CSS source-contract tests with browser measurements; when grouping selectors, update test parsing while preserving the asserted layout properties. When a fixed bar covers content, scroll through the affected region to distinguish temporary occlusion from permanently unreachable controls. Label fixture data and iframe tests explicitly, reuse unchanged real-source evidence, and keep physical-device/native-app verification scoped separately.
10. For isolated component snapshots, read the actual application entrypoint and include its global tokens, component primitives, stylesheet order, and inherited theme variables in the served fixture before acceptance captures. Verify representative computed properties (for example, a production sheet's fixed positioning and the resolved theme token) as well as button background/text colors. Missing global styles can render a working portal as an inline panel or produce white-on-white buttons; classify those captures as harness diagnostics, repair the fixture, and capture again. Label controlled props, clock, and static snapshot interactions explicitly.
11. Treat a nonzero bounding rectangle as a candidate, then check viewport intersection, computed visibility, and `aria-hidden` ancestors. A closed translated sheet can retain its close button's dimensions outside the viewport. Verify the visible main content after dismissal before asserting that the sheet stayed open.

## Minimal measurement recipe

Use a selector created in the owned QA harness:

```js
console.log(await qaPage.evaluate(() => {
  const frame = document.querySelector('#qa-viewport');
  const doc = frame.contentDocument;
  const win = frame.contentWindow;
  return {
    width: win.innerWidth,
    height: win.innerHeight,
    scrollWidth: doc.documentElement.scrollWidth,
    scrollTop: doc.scrollingElement.scrollTop
  };
}));
```

Choose target-control selectors from inspected DOM or fresh snapshot refs. Use `scrollIntoView({block: 'center'})` on an already identified element only for viewport positioning, then measure its rectangle and capture the resulting pixels.

## Floating transport and scrolling-control regression

1. Build a matrix of actual surfaces, transport variants, and desktop/intermediate/mobile widths. Include first render, stopped/playing states, and a full-control to BPM-only transition. Use 1440/768/375px as starting widths and add the product's relevant breakpoints.
2. On each surface, scroll top → middle → bottom → top. After each move, wait for two `requestAnimationFrame` callbacks in the tested window before measuring; immediate reads can capture pending render or scroll work.
3. Record `innerWidth`, `innerHeight`, document `scrollWidth`, `scrollY`, transport count, computed `position`, and `getBoundingClientRect()`. For an always-floating requirement, assert a single fixed transport fully within the viewport from the first render. Compare its bounds across the same surface's scroll sweep to expose reversion to inline placement when scrolling upward.
4. Count each setting control across the whole document, not only inside the bar: exactly one BPM slider, one subdivision select, and zero leftover inline settings panels. A floating bar added beside an existing in-page panel passes every bar-scoped check while the user sees duplicated controls.
5. Verify every button, select, and slider is contained by the bar and reachable at its centre through `document.elementFromPoint`. Also assert useful dimensions against a declared minimum slider-track width, because containment and hit-testing can both pass for a two-pixel slider. Inspect computed grid tracks and winning compound-state/media-query selectors when only one variant collapses; a responsive rule can override its intended columns.
6. Assert labelled buttons are untruncated (`span.scrollWidth <= clientWidth + 1`) at the narrowest width; ellipsis passes containment and hit-testing. For a collapsed `<details>` popover, assert its panel is not rendered while closed, because an author `display:grid` on the panel overrides the native closed state and leaves unreachable controls in the bar. Open it, verify it stays within the viewport, toggle a setting, read it back, then close and confirm the bar height is unchanged.
7. Compare a stable content anchor in document coordinates, such as `element.getBoundingClientRect().top + window.scrollY`, across the scroll sweep. At maximum scroll, confirm final content and actions clear the transport. Inspect existing ancestor bottom padding before adding clearance, because multiple reserves create excessive blank space.
8. Start playback through the real locator, await the rendered playing state, and scroll while it runs. Stop and verify the idle state before changing surfaces. On a BPM-only view, change the value, verify the displayed result, then restore the original setting. Keep audio scheduling or audible-output claims scoped to separately observed evidence.
9. Capture each final variant after the last edit and inspect its pixels. When measurements pass but a control looks collapsed or clipped, add a regression assertion for the missing geometry, fix the cause, and rerun the matrix. Save the reproduction script, measurements, and final captures together.
10. After iframe QA, navigate the owned tab back to the real app route and confirm the native desktop viewport also keeps the transport visible. Preserve user tabs and restore settings changed by the test.

## Self-contained local HTML prototypes

Use this path for a self-contained comparison artifact with inline assets and scripts. Keep routed apps, relative imports, authentication, and backend behavior on their actual served origin.

1. Read the exact delivered HTML through the host file tools and pass its text as data to Aside's direct REPL. Create an owned `about:blank` tab; preserve the user's existing tabs and profile boundaries.
2. Create an iframe in that owned tab with explicit pixel width and height. Set `srcdoc` to the HTML and await the frame's load event before taking the first snapshot. This renders the supplied artifact without a separate local server or file-navigation permission.

```js
await qaPage.evaluate(html => {
  document.body.style.margin = '0';
  document.body.innerHTML = '<iframe id="qa-viewport" style="width:1280px;height:800px;border:0;display:block"></iframe>';
  return new Promise(resolve => {
    const frame = document.querySelector('#qa-viewport');
    frame.onload = () => resolve();
    frame.srcdoc = html;
  });
}, deliveredHtml);
```

3. Resize the iframe itself to exercise its viewport media queries. Measure frame `innerWidth`, `innerHeight`, document `scrollWidth`, and relevant element bounds; scroll the frame document to the task area before capturing it.
4. Prefer frame locator actions. When an observed locator resolves to a non-element, measure the already identified element after `scrollIntoView`, add the iframe's outer offset to its centre coordinates, and use `qaPage.mouse.click`. Read the selected label, content, and styling back after the click.
5. Save captures and measurements together, inspect the pixels, and close only the owned tab. Report the result as controlled browser rendering of the delivered HTML; served-app behavior and device verification have their own evidence paths.

## Blank local preview after rebuilding

1. Read the current page URL and inspect requested script URLs and resource response statuses when the fresh snapshot stays empty.
2. Compare a failing asset URL with the asset path advertised by the served entry HTML. Check the exact script endpoint as well as the entry page, because an HTTP 200 entry document can still load a blank app with script 404s.
3. Navigate through the verified preview entry URL when client-side routing has changed the page pathname and relative assets resolve under a nested route. Confirm the app through a fresh snapshot before resuming QA.
4. Treat this navigation as local-preview recovery. Change router or deployment configuration only when the intended served route reproduces the same failure and the task includes that fix.
