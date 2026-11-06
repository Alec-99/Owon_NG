import hashlib
from pathlib import Path
import struct
import unittest
from PySide6.QtCore import QFile,QIODevice
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from native.app import ScopeWindow
from native.branding import ICON,startup_splash,WORDMARK,BANNER,SPLASH
from native.version import VERSION

ROOT=Path(__file__).resolve().parents[1]
KIT=ROOT/"assets/branding/flow-v2"

class BrandingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app=QApplication.instance() or QApplication([])
    def test_supplied_kit_is_byte_preserved(self):
        lines=(KIT.parent/"flow-v2.sha256").read_text().splitlines()
        self.assertEqual(len(lines),359)
        for line in lines:
            digest,name=line.split("  ",1)
            self.assertEqual(hashlib.sha256((KIT/name).read_bytes()).hexdigest(),digest,name)
    def test_resources_match_original_assets_and_windows_icon_is_multiresolution(self):
        pairs={ICON:"06_PLATFORMS/WINDOWS/owon-ng.ico",
               WORDMARK:"03_LOGOS/wordmark_transparent_on_light_940x220.png",
               BANNER:"04_BANNERS/banner_light_scope_and_wave_1600x347.png",
               SPLASH:"05_SPLASH/LANDSCAPE/splash_dark_no_spinner_1280x720.png"}
        for resource,name in pairs.items():
            file=QFile(resource);self.assertTrue(file.open(QIODevice.ReadOnly))
            self.assertEqual(bytes(file.readAll()),(KIT/name).read_bytes());file.close()
        data=(KIT/pairs[ICON]).read_bytes()
        reserved,kind,count=struct.unpack_from("<HHH",data)
        self.assertEqual((reserved,kind),(0,1));self.assertGreaterEqual(count,5)
        self.assertFalse(QIcon(ICON).isNull())
    def test_native_identity_toolbar_about_and_startup_assets(self):
        w=ScopeWindow();w.timer.stop()
        try:
            self.assertEqual(self.app.applicationName(),"OWON NG")
            self.assertEqual(self.app.applicationVersion(),VERSION)
            self.assertFalse(w.windowIcon().isNull())
            self.assertEqual(w.wordmark.accessibleName(),"OWON NG")
            about=w.about_dialog();self.assertEqual(about.windowTitle(),"Over OWON NG");about.close()
            splash=startup_splash(self.app);self.assertFalse(splash.pixmap().isNull());splash.show();w.show();self.app.processEvents();splash.finish(w);self.assertFalse(splash.isVisible());splash.close()
        finally:w.close()
