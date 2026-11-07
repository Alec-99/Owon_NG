# Native UI visual checks

Owner requirement: capture AND visually inspect screenshots when changing the UI. A passing interaction suite does not establish readable controls.

## Automated cases

scripts/capture_ui.py renders the actual native Qt window in running, paused, UART-decoded, compact (1040x760), imported and profile-popup states. Each is captured with the system palette and with a deliberately inherited dark palette. With branding startup/About checks it writes 16 PNGs, a manifest (OS, Qt platform, scale, dimensions, version) and a versioned ZIP. Only the named screenshot files go into that ZIP. Existing unrelated files in an output directory are not included.

Windows CI runs this on Qt's Windows backend without QT_QPA_PLATFORM=offscreen. Separate visual tests deliberately supply a dark palette and check rendered input contrast, visible dropdown arrows, meaningful acquisition labels and compact window sizing.

After packaging, check_windows_bundle.py starts the actual EXE at normal and 125% scaling. The developer-only --capture-ui option captures its client window, checks the input background/arrow rendering, writes a proof JSON and exits. These checks also verify that the Qt SVG resources are actually included in the frozen application. No full-desktop or hardware capture is taken.

Artifacts:
- Owon_NG-ui-screenshots: raw images and manifests, retained even if later checks fail.
- Owon_NG-native: native packages plus versioned screenshot/proof ZIPs.

## Manual review

Inspect at least the running, decoded, compact, imported/disabled and popup cases. Check text against control backgrounds, selected/disabled/focused distinctions, arrows/checkmarks, clipping, units/labels, source/acquisition state and the next available action. Automated contrast checks cover representative rendered surfaces, not every pixel or all accessibility requirements. The screenshots still require visual review.

## 0.4.2 evidence

The owner's Windows screenshot exposed inherited dark control surfaces combined with fixed dark text. The fix owns the Fusion palette and explicitly styles control states/popups. Local Linux/offscreen screenshots with an inherited dark palette were captured and visually reviewed. This caught missing dropdown arrows and an oversized compact layout; both were corrected and checked again. The startup entrypoint was also exercised at 125% scaling. Windows CI evidence is generated separately; do not describe local offscreen images as reviewed Windows screenshots.

## 0.4.4 selected artwork correction

All 30 automated checks passed; 16 screenshots were captured locally with Linux/Qt offscreen. The running window, compact decoded window with inherited dark palette, imported/disabled state, profile popup and About dialog were visually inspected. The exact selected dark banner fits at 1040x760 and the original named Flow icon is visible in About. Platform conversion is checked against the selected source pixels; Windows CI separately builds and starts the actual EXE. Low-resolution concept sources are retained unchanged; no detail is claimed beyond the supplied artwork.
