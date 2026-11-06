# Version 0.2.0 packaging validation

All three owner-requested formats were built locally: Android debug APK, Python zipapp and Windows x64 EXE. The version in each filename is taken from package.json.

- `npm run check`: production TypeScript/Vite build passed; the three Node test files passed.
- Python zipapp and native Linux build of the shared Go desktop host: actual HTTP requests retrieved the index and referenced JS/CSS assets; missing assets returned 404.
- Windows executable: cross-compiled successfully for windows/amd64; PE signature verified. It has not been launched on Windows.
- Android: Java classes compiled against API 35, converted with D8, packaged, aligned and signed. APK Signature Scheme v2/v3 verification passed. Manifest reports versionName 0.2.0, versionCode 2000, min API 26, target API 35 and the correct launch activity. Bundled web asset bytes are compared against dist.
- No Android device/emulator interaction or Windows device test was available. GitHub Actions execution is not confirmed from this environment.

The APK uses a developer certificate. JSON export is explicitly disabled in the Android UI pending native download handling. Python/Windows open the packaged UI in the system browser and serve it only on loopback. All three contain the same demo frontend; no acquisition, USB or diagnostics engine is included.
