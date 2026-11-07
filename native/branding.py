"""Original user-provided Flow branding, loaded through embedded Qt resources."""
import ctypes
import logging
import sys
from PySide6.QtCore import Qt,QRectF,QSize
from PySide6.QtGui import QIcon,QPainter,QPixmap,QRegion
from PySide6.QtWidgets import QWidget,QSplashScreen
from native import resources_rc
from native.version import VERSION
from native.branding_assets import icon_image

NAME="OWON NG"
ICON=":/owon/brand/app-source.png"
BANNER=":/owon/brand/banner-selected.png"
WORDMARK=BANNER
SPLASH=BANNER
_identity_applied=False

def application_icon():
    return QIcon(QPixmap.fromImage(icon_image(ICON)))

def apply_branding(app):
    global _identity_applied
    app.setApplicationVersion(VERSION)
    app.setApplicationName(NAME)
    app.setApplicationDisplayName(NAME)
    app.setWindowIcon(application_icon())
    if sys.platform=="win32" and not _identity_applied:
        # Stable identity for native taskbar grouping, also when run with Python.
        set_identity=ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID
        set_identity.argtypes=[ctypes.c_wchar_p];set_identity.restype=ctypes.c_long
        result=set_identity("OwonNG.NativeScope")
        if result:
            logging.warning("Windows app identity was not applied: %s",result)
        _identity_applied=True

class BrandImage(QWidget):
    def __init__(self,resource,width,height,parent=None,trim_padding=False):
        super().__init__(parent)
        self.pixmap=QPixmap(resource)
        if self.pixmap.isNull():
            raise RuntimeError("Branding image unavailable: "+resource)
        self.source_rect=self.pixmap.rect()
        if trim_padding and self.pixmap.hasAlphaChannel():
            bounds=QRegion(self.pixmap.mask()).boundingRect()
            if not bounds.isEmpty():self.source_rect=bounds
        self.setFixedSize(width,height)
        self.setAccessibleName(NAME)
        self.setToolTip(NAME)
    def paintEvent(self,event):
        painter=QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        size=self.source_rect.size().scaled(self.size(),Qt.KeepAspectRatio)
        rect=QRectF((self.width()-size.width())/2,(self.height()-size.height())/2,size.width(),size.height())
        painter.drawPixmap(rect,self.pixmap,QRectF(self.source_rect))

def startup_splash(app):
    original=QPixmap(SPLASH)
    if original.isNull():
        raise RuntimeError("Startup image unavailable.")
    screen=app.primaryScreen()
    ratio=screen.devicePixelRatio() if screen else 1
    size=QSize(round(640*ratio),round(121*ratio))
    image=original.scaled(size,Qt.KeepAspectRatio,Qt.SmoothTransformation)
    image.setDevicePixelRatio(ratio)
    splash=QSplashScreen(image)
    splash.setAccessibleName("OWON NG wordt gestart")
    splash.setWindowIcon(application_icon())
    return splash
