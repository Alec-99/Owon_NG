import hashlib
from pathlib import Path
import struct
import tempfile
import unittest
from PySide6.QtCore import QFile,QIODevice,Qt
from PySide6.QtGui import QIcon,QImage
from PySide6.QtWidgets import QApplication
from native.app import ScopeWindow
from native.branding import ICON,startup_splash,WORDMARK,BANNER,SPLASH,application_icon
from native.branding_assets import write_windows_icon,icon_image,ICON_RECT
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
        pairs={ICON:"09_CONCEPT_REFERENCES/selected_reference_1.png",
               BANNER:"09_CONCEPT_REFERENCES/selected_reference_2.png"}
        for resource,name in pairs.items():
            file=QFile(resource);self.assertTrue(file.open(QIODevice.ReadOnly))
            self.assertEqual(bytes(file.readAll()),(KIT/name).read_bytes());file.close()
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"selected.ico"
            write_windows_icon(KIT/pairs[ICON],path)
            data=path.read_bytes()
            embedded=QIcon(str(path))
            self.assertEqual(len(embedded.availableSizes()),7)
            self.assertEqual(embedded.pixmap(256,256).toImage().convertToFormat(QImage.Format_RGB32),icon_image(ICON).scaled(256,256,Qt.IgnoreAspectRatio,Qt.SmoothTransformation).convertToFormat(QImage.Format_RGB32))
        self.assertEqual(icon_image(ICON).size(),ICON_RECT.size())
        self.assertEqual(WORDMARK,BANNER)
        self.assertEqual(SPLASH,BANNER)
        reserved,kind,count=struct.unpack_from("<HHH",data)
        self.assertEqual((reserved,kind),(0,1));self.assertGreaterEqual(count,5)
        self.assertFalse(application_icon().isNull())
    def test_native_identity_toolbar_about_and_startup_assets(self):
        w=ScopeWindow();w.timer.stop()
        try:
            self.assertEqual(self.app.applicationName(),"OWON NG")
            self.assertEqual(self.app.applicationVersion(),VERSION)
            self.assertFalse(w.windowIcon().isNull())
            self.assertEqual(w.wordmark.accessibleName(),"OWON NG")
            self.assertEqual(w.wordmark.pixmap.toImage().convertToFormat(QImage.Format_RGB32),QImage(BANNER).convertToFormat(QImage.Format_RGB32))
            about=w.about_dialog();self.assertEqual(about.windowTitle(),"Over OWON NG");about.close()
            splash=startup_splash(self.app);self.assertFalse(splash.pixmap().isNull());splash.show();w.show();self.app.processEvents();splash.finish(w);self.assertFalse(splash.isVisible());splash.close()
        finally:w.close()
