"""Launch the built EXE at normal/125% scale and check native rendering."""
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import zipfile
root=Path(__file__).resolve().parents[1]
version=runpy.run_path(str(root/"native/version.py"))["VERSION"]
exe=root/"dist"/f"Owon_NG-{version}"/f"Owon_NG-{version}.exe"
if sys.platform!="win32":
    raise SystemExit("Run this check on Windows.")
files=[]
for scale in ("1","1.25"):
    destination=root/"artifacts/ui"/f"windows-packaged-exe-{scale}.png"
    destination.parent.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy();env["QT_SCALE_FACTOR"]=scale
    subprocess.run([str(exe),"--capture-ui",str(destination)],check=True,timeout=60,env=env)
    proof=json.loads(destination.with_suffix(".json").read_text(encoding="utf8"))
    if proof["qt_platform"]!="windows" or proof["version"]!=version or proof.get("application_name")!="OWON NG" or not proof.get("window_icon_sizes"):
        raise SystemExit("Wrong platform or package version in UI proof.")
    files.extend((destination,destination.with_suffix(".json")))
    print("Built Windows EXE rendered and captured:",destination)

with zipfile.ZipFile(root/"artifacts"/f"Owon_NG-{version}-windows-ui-proof.zip","w",zipfile.ZIP_DEFLATED) as bundle:
    for file in files:bundle.write(file,file.name)
