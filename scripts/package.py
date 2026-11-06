"""Build versioned offline launchers after npm run build. No third-party Python deps."""
import json, os, pathlib, shutil, subprocess, zipapp, argparse
root = pathlib.Path(__file__).resolve().parents[1]
version = json.loads((root / "package.json").read_text())["version"]
out = root / "artifacts"
work = root / ".packaging"
if not (root / "dist/index.html").is_file():
    raise SystemExit("Run npm run build first.")
out.mkdir(exist_ok=True)
work.mkdir(exist_ok=True)
parser = argparse.ArgumentParser()
parser.add_argument("target", choices=["python", "windows", "linux", "android"])
target = parser.parse_args().target
def run(*args, **kwargs): subprocess.run(args, check=True, **kwargs)
if target == "python":
    stage = work / "python"
    if stage.exists(): shutil.rmtree(stage)
    stage.mkdir(exist_ok=True)
    shutil.copy(root / "packaging/python/__main__.py", stage)
    shutil.copytree(root / "dist", stage / "web", dirs_exist_ok=True)
    zipapp.create_archive(stage, out / f"Owon_NG-{version}-python.pyz", interpreter="/usr/bin/env python3", compressed=True)
elif target in ("windows", "linux"):
    desktop = root / "packaging/desktop"
    if (desktop / "web").exists(): shutil.rmtree(desktop / "web")
    shutil.copytree(root / "dist", desktop / "web")
    go = os.environ.get("OWON_GO", "go")
    goroot = pathlib.Path(subprocess.check_output([go, "env", "GOROOT"], text=True).strip())
    notices = out / "THIRD_PARTY_NOTICES"
    notices.mkdir(exist_ok=True)
    shutil.copy(goroot / "LICENSE", notices / "Go-LICENSE.txt")
    for licence in (goroot / "src/vendor").rglob("*"):
        if licence.is_file() and licence.name in ("LICENSE", "NOTICE", "COPYING"):
            dest = notices / "Go-vendor" / licence.relative_to(goroot / "src/vendor")
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(licence, dest)
    env = os.environ | {"GOOS": target, "GOARCH": "amd64", "CGO_ENABLED": "0", "GOTOOLCHAIN": "local"}
    suffix = "windows-x64.exe" if target == "windows" else "linux-x64"
    run(os.environ.get("OWON_GO", "go"), "build", "-trimpath", "-ldflags", f"-s -w -X main.version={version}", "-o", str(out / f"Owon_NG-{version}-{suffix}"), ".", cwd=desktop, env=env)
else:
    sdk = pathlib.Path(os.environ["ANDROID_HOME"])
    tools = sdk / "build-tools/35.0.0"
    jar = sdk / "platforms/android-35/android.jar"
    stage = work / "android"
    if stage.exists(): shutil.rmtree(stage)
    classes = stage / "classes"
    dex = stage / "dex"
    for d in (stage, classes, dex): d.mkdir(exist_ok=True)
    shutil.copytree(root / "dist", stage / "assets/web", dirs_exist_ok=True)
    # Stable application ID; versionCode maps three numeric semver components.
    major, minor, patch = map(int, version.split("."))
    code = major * 1000000 + minor * 1000 + patch
    manifest = stage / "AndroidManifest.xml"
    manifest.write_text(f'''<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="nl.owon.ng" android:versionCode="{code}" android:versionName="{version}"><uses-sdk android:minSdkVersion="26" android:targetSdkVersion="35"/><application android:label="Owon NG {version} DEMO" android:theme="@android:style/Theme.Material.NoActionBar" android:allowBackup="false" android:supportsRtl="true" android:usesCleartextTraffic="false"><activity android:name=".MainActivity" android:exported="true" android:configChanges="orientation|screenSize"><intent-filter><action android:name="android.intent.action.MAIN"/><category android:name="android.intent.category.LAUNCHER"/></intent-filter></activity></application></manifest>''')
    unsigned = stage / "unsigned.apk"
    run(str(tools / "aapt2"), "link", "-I", str(jar), "--manifest", str(manifest), "-A", str(stage / "assets"), "-o", str(unsigned))
    run("java", "-m", "jdk.compiler/com.sun.tools.javac.Main", "-source", "8", "-target", "8", "-bootclasspath", str(jar), "-d", str(classes), str(root / "packaging/android/src/nl/owon/ng/MainActivity.java"))
    run(str(tools / "d8"), "--lib", str(jar), "--min-api", "26", "--output", str(dex), *map(str, classes.rglob("*.class")))
    import zipfile
    with zipfile.ZipFile(unsigned, "a", zipfile.ZIP_DEFLATED) as apk: apk.write(dex / "classes.dex", "classes.dex")
    aligned = stage / "aligned.apk"
    run(str(tools / "zipalign"), "-f", "4", str(unsigned), str(aligned))
    key = pathlib.Path(os.environ.get("OWON_DEBUG_KEY", str(pathlib.Path.home() / ".android/owon-debug.keystore")))
    if not key.exists():
        key.parent.mkdir(parents=True, exist_ok=True)
        run("keytool", "-genkeypair", "-keystore", str(key), "-storepass", "android", "-keypass", "android", "-alias", "androiddebugkey", "-dname", "CN=Owon NG Debug", "-keyalg", "RSA", "-validity", "10000")
    output = out / f"Owon_NG-{version}-android-debug.apk"
    run(str(tools / "apksigner"), "sign", "--v4-signing-enabled", "false", "--ks", str(key), "--ks-pass", "pass:android", "--out", str(output), str(aligned))
    run(str(tools / "apksigner"), "verify", "--verbose", str(output))
print("Built", target, "version", version, "in", out)
