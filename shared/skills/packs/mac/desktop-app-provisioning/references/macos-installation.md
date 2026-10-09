# macOS signed DMG installation

Use this recipe after resolving the live official download URL and confirming the user authorized installation. The attach, signature assessment, bundle copy, detached image, and executable process check were exercised successfully; no browser integration is implied.

1. Discover architecture with `uname -m`, OS with `sw_vers`, and whether the intended destination already exists.
2. Inspect redirects with `curl -fIL --max-time 30 "$URL"`; download with `curl -fL --retry 2 --max-time 180 "$URL" -o "$SCRATCH/installer.dmg"`.
3. Attach with `hdiutil attach "$SCRATCH/installer.dmg" -nobrowse -readonly -plist`. Parse the returned plist for the mounted volume; inspect its contents for the actual app bundle rather than assuming the volume or bundle name.
4. Verify the source bundle with `codesign --verify --deep --strict --verbose=2 "$SOURCE_APP"` and `spctl --assess --type execute --verbose=2 "$SOURCE_APP"`. Require a passing assessment; do not disable Gatekeeper or remove quarantine to force a failed installer through.
5. Copy with `ditto "$SOURCE_APP" "$DEST_APP"` only after checking the destination does not contain an installation that would be overwritten. Detach the exact volume with `hdiutil detach "$MOUNT_POINT"`.
6. Read `Contents/Info.plist` for `CFBundleShortVersionString` and `CFBundleIdentifier`. Launch with `open -g "$DEST_APP"` when preserving foreground work, then verify the exact bundle's executable process with `pgrep -fl` and, when needed, an app-scoped native capture.

Do not call `open -g` a verified focus-preservation test. It avoids requesting activation, but the launched app may still activate itself. Measure foreground state when no-focus operation is part of acceptance.
