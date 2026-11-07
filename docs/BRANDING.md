# OWON NG Flow branding

The owner supplied owon-ng-flow-final-v2.zip and explicitly requested repository inclusion and application integration. All 359 files are preserved byte-for-byte under assets/branding/flow-v2, including source vectors, rendered variants, platform assets, examples, concepts and the supplied documentation. IMPORT.json records the archive checksum; flow-v2.sha256 records every extracted file. Git attributes preserve text line endings as supplied.

Archive documentation is advisory brand/reference material. No scripts, web/Android manifests, desktop examples or store placeholders from the archive are executed, deployed or presented as actual application screenshots.

Active integration (owner correction, 0.4.4):
- The owner selected the exact artwork in 09_CONCEPT_REFERENCES/selected_reference_1.png and selected_reference_2.png, rather than the visibly different reconstructed production exports.
- Native window/taskbar icon, About icon and Windows EXE resource: reference 1. Runtime uses the square rectangle (10, 0, 132, 132), excluding its printed caption. scripts/package.py uses native/branding_assets.py to convert this same square into a seven-resolution ICO with Qt. No artwork is redrawn and no extra image dependency is required. The source is small; upscaling cannot supply additional detail.
- Toolbar, About dialog and brief startup image: the exact dark horizontal banner in reference 2, fitted proportionally. The original has a narrow white outer border, which is retained.
- README: 07_SOCIAL_REPOSITORY/readme_header_1600x480.png.

Original files, including concepts and all previous exports, remain byte-for-byte intact. Asset documents are reference material; this selection follows the owner's explicit request.

Runtime assets are embedded in native/resources.qrc and generated resources_rc.py. Regenerate after resource changes with pyside6-rcc native/resources.qrc -o native/resources_rc.py. The source distribution includes the complete kit; Windows ships only its embedded runtime assets and source notes. Existing channel colors and readable control contrast are retained.

Original PNG exports are used to preserve the supplied typography without adding fonts. Other platform exports are available for later native Android/macOS/Linux/store work; their presence does not establish platform support. Store screenshot placeholders are not used as production app UI.

The owner has authorized use in this project. No additional third-party reuse licence or manufacturer affiliation is asserted; the original SOURCE_NOTES and brandbook are retained.
