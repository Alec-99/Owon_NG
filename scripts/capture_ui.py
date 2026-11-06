"""Capture native Qt states for visual review, including inherited dark palettes."""
import argparse
import json
from pathlib import Path
import platform
import zipfile
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from PySide6.QtCore import Qt, qVersion
from PySide6.QtGui import QColor, QPalette
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication
from native.app import ScopeWindow
from native.branding import startup_splash
from native.version import VERSION

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",default=str(ROOT/"artifacts/ui"))
    args=parser.parse_args()
    output=Path(args.output);output.mkdir(parents=True,exist_ok=True)
    app=QApplication([])
    records=[]
    system_palette=QPalette(app.palette())
    for seed in ("system","dark-inherited"):
        if seed=="system":
            app.setPalette(system_palette)
        else:
            dark=QPalette()
            for group in (QPalette.Active,QPalette.Inactive,QPalette.Disabled):
                for role in (QPalette.Window,QPalette.Base,QPalette.Button):
                    dark.setColor(group,role,QColor("#252525"))
                for role in (QPalette.Text,QPalette.ButtonText,QPalette.WindowText):
                    dark.setColor(group,role,QColor("#f2f2f2"))
            app.setPalette(dark)
            app.styleHints().setColorScheme(Qt.ColorScheme.Dark)
        splash=startup_splash(app);splash.show();app.processEvents()
        name=f"{seed}-startup.png"
        if not splash.grab().save(str(output/name)):raise RuntimeError("Could not capture startup")
        records.append({"file":name,"state":"startup","inherited_palette":seed})
        window=ScopeWindow()
        window.timer.stop()
        window.profile.setCurrentText("PWM")
        window.show();splash.finish(window);QTest.qWait(120)
        def capture(state):
            app.processEvents()
            name=f"{seed}-{state}.png"
            if not window.grab().save(str(output/name)):
                raise RuntimeError("Could not save UI screenshot")
            records.append({"file":name,"size":[window.width(),window.height()],
                            "scale":window.devicePixelRatioF(),"state":state,
                            "inherited_palette":seed})
        try:
            capture("running")
            window.toggle_run();capture("paused")
            window.profile.setCurrentText("UART 8N1")
            window.time.setValue(.5);window.analyse();capture("uart-decoding")
            window.resize(1040,760);app.processEvents();capture("compact")
            with tempfile.TemporaryDirectory() as tmp:
                recording=Path(tmp)/"demo.json"
                window.capture.save(recording,"Opgeslagen voorbeeld",window.view_state())
                window.read_capture(recording);capture("imported")
            about=window.about_dialog();about.show();QTest.qWait(60)
            name=f"{seed}-about.png"
            if not about.grab().save(str(output/name)):raise RuntimeError("Could not capture About")
            records.append({"file":name,"state":"about","inherited_palette":seed})
            about.close()
            window.profile.showPopup();QTest.qWait(60)
            name=f"{seed}-profile-popup.png"
            if not window.profile.view().window().grab().save(str(output/name)):
                raise RuntimeError("Could not capture profile popup")
            records.append({"file":name,"state":"profile-popup","inherited_palette":seed})
            window.profile.hidePopup()
        finally:
            window.close()
    manifest={"version":VERSION,"os":platform.system(),"qt":qVersion(),
              "qt_platform":app.platformName(),"screenshots":records,
              "note":"Qt widget captures, not screenshots of the entire OS desktop. Review remains necessary."}
    (output/"manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf8")
    archive=ROOT/"artifacts"/f"Owon_NG-{VERSION}-ui-screenshots"
    with zipfile.ZipFile(str(archive)+".zip","w",zipfile.ZIP_DEFLATED) as bundle:
        for name in [r["file"] for r in records]+["manifest.json"]:
            bundle.write(output/name,name)
    print(f"Captured {len(records)} screenshots using {app.platformName()}: {archive}.zip")

if __name__=="__main__":
    main()
