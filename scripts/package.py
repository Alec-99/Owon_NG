"""Build native distributions without browser or HTTP server."""
import argparse,pathlib,shutil,subprocess,sys,zipfile,importlib.metadata,runpy
root=pathlib.Path(__file__).resolve().parents[1];version=runpy.run_path(str(root/'native/version.py'))['VERSION'];out=root/'artifacts';out.mkdir(exist_ok=True)
brand=root/'assets/branding/flow-v2';icon=out/'owon-ng-selected.ico'
p=argparse.ArgumentParser();p.add_argument('target',choices=['python','windows','android']);args=p.parse_args()
if args.target=='android':raise SystemExit('Native Android is not implemented; the old WebView APK is retired.')
if args.target=='python':
 with zipfile.ZipFile(out/f'Owon_NG-{version}-python-native.zip','w',zipfile.ZIP_DEFLATED) as z:
  for f in [root/'app.py',root/'requirements-native.txt',root/'docs/NATIVE_APP.md',root/'docs/ACQUISITION_CORE.md',root/'docs/HARDWARE_VALIDATION.md',root/'docs/VISUAL_QA.md',root/'docs/BRANDING.md',root/'assets/branding/IMPORT.json',root/'assets/branding/flow-v2.sha256',root/'native/resources.qrc',*sorted((root/'native').glob('*.py')),*sorted((root/'native/assets').glob('*'))]:z.write(f,f.relative_to(root))
  for f in sorted(brand.rglob('*')):
   if f.is_file():z.write(f,f.relative_to(root))
else:
 if sys.platform!='win32':raise SystemExit('Build Windows EXE on Windows with the Native app packages workflow.')
 sys.path.insert(0,str(root))
 from native.branding_assets import write_windows_icon
 write_windows_icon(brand/'09_CONCEPT_REFERENCES/selected_reference_1.png',icon)
 subprocess.run([sys.executable,'-m','PyInstaller','--noconfirm','--clean','--windowed','--onedir','--icon',str(icon),'--name',f'Owon_NG-{version}','app.py'],cwd=root,check=True)
 stage=root/'dist'/f'Owon_NG-{version}';shutil.copy(root/'docs/NATIVE_APP.md',stage/'LEESMIJ.md')
 shutil.copy(root/'docs/HARDWARE_VALIDATION.md',stage/'HARDWARE_VALIDATION.md')
 for name in ('ACQUISITION_CORE.md','VISUAL_QA.md','BRANDING.md'):shutil.copy(root/'docs'/name,stage/name)
 shutil.copy(brand/'00_README_FIRST/SOURCE_NOTES.md',stage/'BRAND_SOURCE_NOTES.md')
 notices=stage/'THIRD_PARTY_NOTICES';notices.mkdir(exist_ok=True)
 for package in ('PySide6','PySide6_Essentials','PySide6_Addons','shiboken6'):
  d=importlib.metadata.distribution(package)
  for f in d.files or []:
   if 'licenses' in str(f).lower() or f.name.lower().startswith(('license','copying','notice')):
    source=pathlib.Path(d.locate_file(f))
    if source.is_file():
     dest=notices/package/pathlib.Path(str(f));dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy(source,dest)
 shutil.make_archive(str(out/f'Owon_NG-{version}-windows-x64'),'zip',stage.parent,stage.name)
print('Native package built:',args.target)
