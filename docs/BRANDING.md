# OWON NG Flow branding

The owner supplied owon-ng-flow-final-v2.zip and explicitly requested repository inclusion and application integration. All 359 files are preserved byte-for-byte under assets/branding/flow-v2, including source vectors, rendered variants, platform assets, examples, concepts and the supplied documentation. IMPORT.json records the archive checksum; flow-v2.sha256 records every extracted file. Git attributes preserve text line endings as supplied.

Archive documentation is advisory brand/reference material. No scripts, web/Android manifests, desktop examples or store placeholders from the archive are executed, deployed or presented as actual application screenshots.

Active integration:
- Native app/window/taskbar icon and Windows EXE resource: 06_PLATFORMS/WINDOWS/owon-ng.ico (multi-resolution compact mark).
- Workbar: 03_LOGOS/wordmark_transparent_on_light_940x220.png.
- About dialog: 04_BANNERS/banner_light_scope_and_wave_1600x347.png.
- Startup: 05_SPLASH/LANDSCAPE/splash_dark_no_spinner_1280x720.png, only while the native interface initializes, without an artificial delay.
- README: 07_SOCIAL_REPOSITORY/readme_header_1600x480.png.

Only transparent outer padding is omitted when fitting the toolbar wordmark; the original image bytes remain unchanged.

Runtime assets are embedded in native/resources.qrc and generated resources_rc.py. Regenerate after resource changes with pyside6-rcc native/resources.qrc -o native/resources_rc.py. The source distribution includes the complete kit; Windows ships only its embedded runtime assets and source notes. Existing channel colors and readable control contrast are retained.

Original PNG exports are used to preserve the supplied typography without adding fonts. Other platform exports are available for later native Android/macOS/Linux/store work; their presence does not establish platform support. Concept references and screenshot placeholders are not used as production app UI.

The owner has authorized use in this project. No additional third-party reuse licence or manufacturer affiliation is asserted; the original SOURCE_NOTES and brandbook are retained.
