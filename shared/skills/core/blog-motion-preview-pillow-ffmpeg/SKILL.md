---
name: blog-motion-preview-pillow-ffmpeg
description: "Use when making a short silent GIF/MP4 motion for a blog."
---

# Short silent motion preview (5–8s) with Pillow + ffmpeg

Render Korean-labelled frames with Pillow, encode with ffmpeg, verify by decoding the output.

## Workflow
1. Pull every number from the post's research/draft and re-verify against the official page (`curl -sL -A Mozilla ... | grep`), never from memory.
2. Script `scripts/render_<topic>_motion.py`: 1536×1024, 30fps, `frames = fps*duration`; `ease_out` + `seg(t,start,end)` helpers; draw per-frame PNGs to `$TMPDIR/<name>_frames`.
3. Run without touching the repo env: `uv run --no-project --with pillow python script.py <frames_dir>` (plain `uv run` creates `.venv` in the repo — delete it if that happens).
4. Korean font on macOS: `ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc', size, index=6)` (6=Bold, 4=SemiBold, 0=Regular).
5. Encode: MP4 `ffmpeg -framerate 30 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 20 -movflags +faststart -an`; GIF `-vf "fps=15,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer:bayer_scale=3" -loop 0`.
6. Verify with `ffprobe -count_frames` (nb_read_frames, duration, codec_type=video only) and decode frames from the MP4/GIF (`ffmpeg -ss T -i out -frames:v 1`) for visual review — review the encoded output, not just source PNGs.

## Color direction

- Pick colors per article: open THAT post's actual hero/body/promo images first and derive the palette from them. Body-image colors differ every post (`앞으로 본문이미지 색상이 계속 달라질거니까 잘맞춰서해`), so never carry a previous post's green/oak or any universal palette forward.
- User preference: `색감은 이미지랑 같이가야돼 나는 물빠진색감은싫어해`. Avoid washed-out/pastel palettes; use clear saturated colors and strong label/bar contrast while preserving the factual text and timing. For an authorized color revision, rerender actual GIF/MP4 without an intermediate approval request and inspect decoded early/mid/final frames.

## On-screen text and geometry

- Put only reader-useful comparison facts on screen (e.g. `펼친 길이 FROST 134cm · MULIG 173cm`). Never add production-meta caveats such as `모양은 설명용 그림이에요` — the user rejected that outright (`이런건하지마 대체왜있는거야`); such lines are agent self-justification, not information.
- If the product mechanism can't be drawn accurately, don't draw it: use plain length bars / numeric comparison instead of invented unfolding geometry. Then no geometry caveat is needed.

## Naver blog insertion (Aside REPL)

- Open `PostUpdateForm.naver?blogId=<id>&logNo=<logNo>` for in-place edit; verify owner first on the public post (`수정하기` button + nick). Place the caret via DOM Range at the end of the target paragraph, then `page.waitForEvent('filechooser')` + click `.se-toolbar button[data-name="image"]` + `fc.setFiles('artifacts/<sub>/<file>.gif')`.
- Aside rejects file paths outside `~/.aside/u/<n>/sessions/<sid>/`; `fs.resolvePath('artifacts/x')` gives the absolute dir to `cp` into. `page.waitForTimeout` is undefined in this REPL — use a `setTimeout` sleep.
- Toggle `.se-set-ai-mark-button-toggle` on the new component (expect `se-is-selected`), click `.se-caption` and `keyboard.insertText` the caption. Publish: `button.publish_btn__v_kS9` → check 공개/검색 radios unchanged → `button.confirm_btn__byZZW`; success returns PostView with `isAfterUpdateOnly=true`.
- Public viewer renders GIFs as `<video class="_gifmp4">` (`?type=mp4w800`, loop, muted) and does NOT draw `.se-ai-tooltip-container` on them; verify the AI mark by reopening the editor, and verify the file by `data-linkdata.fileSize` matching the local byte size. Iframe contexts go stale after publish — `page.goto` the PostView.naver URL directly for readback.

## Pitfalls
- `$TMPDIR` in some agent terminals resolves to the system temp dir, not the executor's scratch dir; use the printed absolute path for vision checks.
- Label collisions appear only at specific timestamps: check an early, a mid, and the final frame.
