# OWON NG — FLOW BRANDBOOK v2

Final brand direction: **B — Golf / Flow**, with the **OWON NG / owonNG name kept in the primary app icon, wordmarks, banners, splash screens and store art**.

Selected inspirations:
- Orange flowing wave and dark navy-gray base
- A classic oscilloscope display on the broad logo banner
- Two dark splash styles: clean / cinematic and technical cyan-screen

## Where to start
1. `00_README_FIRST/preview.png` — overview of the actual files.
2. `01_VECTOR_MASTERS` — editable SVG source designs; colors, text and paths can be modified.
3. `02_ICONS/APP_PNG` — square app icons with `owonNG` name, dark/light/round.
4. `02_ICONS/TRANSPARENT` — glyph-only and monochrome on transparent background.
5. `03_LOGOS` — **name-bearing** wordmarks for dark or light surfaces.
6. `04_BANNERS` — horizontal branded banners with scope icon and wave trace.
7. `05_SPLASH` — dark, light, technical and portrait splash screens.
8. `06_PLATFORMS` — platform presets for Android, Windows, macOS, iOS, Linux, web/PWA.
9. `07_SOCIAL_REPOSITORY` — GitHub, OG and readme images.
10. `08_STORE_ASSETS` — store icons and placeholders clearly marked for actual app screenshots.
11. `09_CONCEPT_REFERENCES` — the four low-resolution selections provided in the conversation, NOT the production masters.

## Name rule
Use **OWON NG** in product text, and the styled **owonNG** wordmark (white / charcoal `owon`, orange `NG`) in visual material. Avoid replacing the name with a mere signal/wave in banners or splash screens. Compact / adaptive icons can use only the wave where OS masking or small dimensions would make the wordmark illegible; the name-bearing alternatives are also included.

## How to integrate
- Android: copy `06_PLATFORMS/ANDROID/app/src/main/res` into your Android module's `src/main/res`. Confirm drawable and mipmap names do not clash with your existing assets; the included XML uses `@color/owon_ng_launcher_bg`.
- Windows: use `06_PLATFORMS/WINDOWS/owon-ng.ico`; MSIX assets under `WINDOWS/MSIX/Assets` can be referenced by your app manifest.
- macOS: use `06_PLATFORMS/MACOS/owon-ng.icns` or the `.iconset`.
- Linux: copy the `hicolor` icon tree and adapt `owon-ng.desktop.example`.
- iOS: copy `IOS/Assets.xcassets/AppIcon.appiconset` into an Xcode project, set AppIcon.
- Web: copy files under `WEB` to a public asset directory and adapt example-head.html and site.webmanifest paths.
- App stores: review specifications before final release, as marketplace requirements evolve. Screenshot files here are clearly marked templates, not real captures.

## Colors
- Orange `#FF8900`
- Deep orange `#E96700`
- Graphite dark `#101720`
- Deep dark `#080D14`
- Light `#F5F7FA`
- Technical cyan `#23B6F0` (technical-only accent)

## Sources / fidelity
Visuals are hand-reconstructed vector artwork based on the *selected direction*, not pixel-for-pixel upscales of the small concept screenshots. The design assets are editable SVGs, with pre-rendered PNG, WebP, JPEG, ICO and ICNS exports.

## Note on trademark
This is branding for an independently developed OWON NG software project. It does not claim official manufacturer endorsement or affiliation.
