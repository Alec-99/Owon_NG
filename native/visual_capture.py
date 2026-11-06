"""Opt-in capture of the actual application window for packaged-app QA."""
import json
from pathlib import Path
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QApplication
from native.version import VERSION

def schedule_capture(window,app,destination):
    destination=Path(destination)
    def capture():
        code=1
        try:
            destination.parent.mkdir(parents=True,exist_ok=True)
            app.processEvents()
            if not window.grab().save(str(destination),"PNG"):
                raise RuntimeError("Window capture failed")
            controls=[]
            for name,widget in (("profile",window.profile),("timebase",window.time),("scale",window.channel_scales[0])):
                image=widget.grab().toImage()
                scale=image.devicePixelRatio()
                surface=image.pixelColor(round(max(4,widget.width()-35)*scale),round((widget.height()-6)*scale))
                # The original regression was a dark control surface with dark text.
                if surface.lightnessF()<.7:
                    raise RuntimeError(f"Dark/unreadable control surface: {name}")
                arrow_pixels=sum(image.pixelColor(x,y).lightnessF()<.35
                    for x in range(round((widget.width()-17)*scale),round((widget.width()-6)*scale))
                    for y in range(round((widget.height()/2-4)*scale),round((widget.height()/2+4)*scale))) if name!="timebase" else None
                if arrow_pixels is not None and arrow_pixels<4:
                    raise RuntimeError(f"Missing dropdown chevron: {name}")
                controls.append({"name":name,"background":surface.name(),
                                 "text":widget.palette().color(QPalette.Text).name(),
                                 "arrow_pixels":arrow_pixels})
            proof={"version":VERSION,"qt_platform":app.platformName(),
                   "window":[window.width(),window.height()],"device_scale":window.devicePixelRatioF(),"controls":controls,
                   "scope":"Native window only; no desktop or hardware capture."}
            destination.with_suffix(".json").write_text(json.dumps(proof,indent=2),encoding="utf8")
            code=0
        except Exception as error:
            destination.with_suffix(".error.txt").write_text(str(error),encoding="utf8")
        finally:
            window.close()
            app.exit(code)
    QTimer.singleShot(500,capture)
