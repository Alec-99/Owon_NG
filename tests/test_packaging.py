"""Functional requests against packaged launchers; binaries must be built first."""
import json
import os
import pathlib
import re
import subprocess
import sys
import unittest
import urllib.request
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
VERSION = json.loads((ROOT / "package.json").read_text())["version"]

class LaunchTests(unittest.TestCase):
    def check_launcher(self, command):
        env = os.environ | {"OWON_NO_BROWSER": "1", "BROWSER": "true"}
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env) as proc:
            try:
                line = proc.stdout.readline()
                url = re.search(r"http://127.0.0.1:\d+/", line)
                self.assertIsNotNone(url, line)
                # Never send loopback test requests to a network proxy.
                opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
                html = opener.open(url[0], timeout=5).read().decode()
                self.assertIn('<html lang="nl">', html)
                assets = re.findall(r'(?:src|href)="([^"]+\.(?:js|css))"', html)
                self.assertGreaterEqual(len(assets), 2)
                for asset in assets:
                    response = opener.open(url[0] + asset.lstrip("/"), timeout=5)
                    self.assertEqual(response.status, 200)
                    self.assertGreater(len(response.read()), 100)
                missing = url[0] + "missing-ui-asset.js"
                with self.assertRaises(urllib.error.HTTPError) as error:
                    opener.open(missing, timeout=5)
                self.assertEqual(error.exception.code, 404)
            finally:
                proc.terminate()
                proc.wait(timeout=5)

    def test_python_archive(self):
        self.check_launcher([sys.executable, str(ROOT / f"artifacts/Owon_NG-{VERSION}-python.pyz")])

    @unittest.skipUnless(sys.platform.startswith("linux"), "Linux native host smoke test")
    def test_native_host(self):
        self.check_launcher([str(ROOT / f"artifacts/Owon_NG-{VERSION}-linux-x64")])

    def test_android_assets(self):
        with zipfile.ZipFile(ROOT / f"artifacts/Owon_NG-{VERSION}-android-debug.apk") as apk:
            self.assertIn("classes.dex", apk.namelist())
            self.assertIn("AndroidManifest.xml", apk.namelist())
            for name in (ROOT / "dist").rglob("*"):
                if name.is_file():
                    self.assertEqual(apk.read("assets/web/" + name.relative_to(ROOT / "dist").as_posix()), name.read_bytes())

    def test_windows_pe(self):
        binary = (ROOT / f"artifacts/Owon_NG-{VERSION}-windows-x64.exe").read_bytes()
        self.assertEqual(binary[:2], b"MZ")
        offset = int.from_bytes(binary[60:64], "little")
        self.assertEqual(binary[offset:offset+4], b"PE\x00\x00")

if __name__ == "__main__":
    unittest.main()
