import sys, math
from PySide6.QtWidgets import (QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QListWidget,QStackedWidget,QLabel,QPushButton,QComboBox,QDoubleSpinBox,QCheckBox,QSlider,QTextEdit,QFileDialog,QMessageBox,QGroupBox,QFormLayout,QSplitter,QDialog,QDialogButtonBox,QScrollArea,QTableWidget,QTableWidgetItem,QHeaderView,QAbstractItemView)
from PySide6.QtCore import Qt,QTimer
from native.model import PROFILES,WARNING,fixture,load
from native.canvas import ScopeCanvas
from native.decoding import decode_capture
from native.acquisition import Acquisition
from native.capture import ViewState
from native.recording import load_recording

from native.version import VERSION
PAGES=["Automotive","Elektronica","Vrij meten","Bibliotheek","Opnames / Geschiedenis","Rapporten","Instellingen","Help"]
from native.layout import STYLE, shell, scope
def button(text,fn):
 b=QPushButton(text);b.clicked.connect(fn);return b
def group(title):
 g=QGroupBox(title);l=QVBoxLayout(g);return g,l

class ScopeWindow(QMainWindow):
 def __init__(self):
  super().__init__()
  self.setWindowTitle(f"Owon NG {VERSION} — native oscilloscoop · DEMO")
  self.resize(1440,960);self.running=True;self.saved=[];self.capture=fixture("CKP inductief")
  content=shell(self,button,PAGES,VERSION)
  self.pages=QStackedWidget();content.addWidget(self.pages,1)
  self.scope=self.make_scope();self.pages.addWidget(self.scope)
  self.library=self.make_library();self.pages.addWidget(self.library)
  self.history=QListWidget();self.history.addItem("Nog geen lokaal opgeslagen opnames.");self.history.itemDoubleClicked.connect(self.open_history);self.pages.addWidget(self.history)
  self.report=QTextEdit();self.report.setReadOnly(True);self.pages.addWidget(self.report)
  settings=QLabel("Hardware niet verbonden.\nUSB, extra decoders en gevalideerde diagnostiek worden later toegevoegd. De eerste offline UART/I²C/PWM-analyse staat in de scopeweergave.\n\nDeze app toont uitsluitend synthetische fixtures en geïmporteerde demo-opnames.");settings.setWordWrap(True);self.pages.addWidget(settings)
  help_page=QTextEdit();help_page.setReadOnly(True);help_page.setPlainText("Bediening\n\nStart/Pauze bestuurt de simulatie. Single maakt één nieuwe demo-frame.\nSleep cursors A/B in de grafiek; links/rechts bestuurt cursor A, Shift+links/rechts cursor B. Het muiswiel zoomt in tijd.\n\nV/div verandert de weergave, niet de samples. Tijdzoom en verschuiving houden de sampletijd intact.\n\nBewaar/Open gebruikt een versiegebonden JSON-bestand met herkomst en notitie.\n\n"+WARNING);self.pages.addWidget(help_page)
  self.nav.currentRowChanged.connect(self.navigate);self.nav.setCurrentRow(0)
  self.acquisition=Acquisition();self.acquisition.configure(self.profile.currentText(),self.running)
  self.timer=QTimer(self);self.timer.timeout.connect(self.frame);self.timer.start(50)
  self.statusBar().showMessage("DEMO — geen hardware verbonden | Triggers en automatische diagnose niet beschikbaar")
  self.refresh_metrics()
 def make_scope(self):
  return scope(self,button)
 def make_library(self):
  w=QWidget();l=QVBoxLayout(w);l.addWidget(QLabel("Testbibliotheek — illustratieve profielen, geen bekende-goede voertuigmetingen"))
  table=QTableWidget(len(PROFILES),3);table.setHorizontalHeaderLabels(["Component / signaal","Werkgebied","Toepassing"])
  table.setSelectionBehavior(QAbstractItemView.SelectRows);table.setSelectionMode(QAbstractItemView.SingleSelection);table.setEditTriggers(QAbstractItemView.NoEditTriggers)
  names=list(PROFILES)
  for row,name in enumerate(names):
   category,_,desc,_=PROFILES[name]
   for col,value in enumerate((name,category,desc)):table.setItem(row,col,QTableWidgetItem(value))
  table.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents);table.horizontalHeader().setSectionResizeMode(1,QHeaderView.ResizeToContents);table.horizontalHeader().setStretchLastSection(True)
  table.verticalHeader().hide();table.selectRow(0);table.cellDoubleClicked.connect(lambda row,col:self.choose_from_library(names[row]))
  l.addWidget(table);l.addWidget(button("Open geselecteerd profiel",lambda:self.choose_from_library(names[table.currentRow()]) if table.currentRow()>=0 else None));return w
 def choose_from_library(self,name):
  self.nav.setCurrentRow(0 if PROFILES[name][0]=="Automotive" else 1);self.profile.setCurrentText(name)
 def navigate(self,row):
  if row<3:
   self.modes.blockSignals(True);self.modes.setCurrentIndex(row);self.modes.blockSignals(False)
  if row<3:
   self.pages.setCurrentIndex(0)
   if row==0 and PROFILES[self.profile.currentText()][0]!="Automotive":self.profile.setCurrentText("CKP inductief")
   if row==1 and PROFILES[self.profile.currentText()][0]!="Elektronica":self.profile.setCurrentText("PWM")
  elif row==3:self.pages.setCurrentIndex(1)
  elif row==4:self.pages.setCurrentIndex(2)
  elif row==5:
   self.report.setPlainText("DEMO-RAPPORT — geen diagnose\n\nProfiel: "+self.capture.profile+"\nHerkomst: "+self.capture.source+"\n\nObservatie:\n"+self.note.toPlainText()+"\n\n"+WARNING);self.pages.setCurrentIndex(3)
  elif row==6:self.pages.setCurrentIndex(4)
  else:self.pages.setCurrentIndex(5)
 def select_profile(self,name):
  category=0 if PROFILES[name][0]=="Automotive" else 1
  if self.nav.currentRow() in (0,1) and self.nav.currentRow()!=category:self.nav.setCurrentRow(category)
  if hasattr(self,"acquisition"):self.acquisition.configure(name,self.running)
  self.canvas.decode_result=None;self.analysis_result.setText("Nieuw profiel: kies een decoder en analyseer de samples.")
  self.capture=fixture(name);self.canvas.capture=self.capture;self.provenance.setText("DEMO · GESIMULEERD");self.canvas.update();self.update_guide();self.refresh_metrics()
 def update_guide(self):
  name=self.profile.currentText();_,_,desc,safety=PROFILES[name]
  self.guide.setText(desc+"\n\n1. Kies dit demo-profiel.\n2. Lees aansluitwaarschuwingen.\n3. Bekijk de illustratieve referentie.\n4. Pauzeer, verplaats cursors en voeg een notitie toe.\n5. Bewaar de demo-opname.\n\n"+safety+"\n\nAfwijkingen geven hier geen foutdiagnose.")
 def apply_preset(self):
  self.time.setValue(500 if self.profile.currentText()=="Lambda narrowband" else 10);self.pan.setValue(0);self.select_profile(self.profile.currentText())
 def channel_visible(self,c,v):self.canvas.visible[c]=v;self.canvas.update()
 def scale_changed(self,c,v):self.canvas.scales[c]=v;self.canvas.update()
 def offset_changed(self,c,v):self.canvas.offsets[c]=v;self.canvas.update()
 def time_changed(self,v):self.canvas.time_div=v/1000;self.canvas.update();self.refresh_metrics()
 def pan_changed(self,v):self.canvas.pan=v/1000;self.canvas.update();self.refresh_metrics()
 def toggle_run(self):
  if self.capture.source=="import":
   self.explain("Geïmporteerde opname","De opgeslagen samples blijven ongewijzigd. Kies een demo-profiel om nieuwe samples te genereren.","Opname- en weergave-instellingen worden afzonderlijk bewaard.");return
  self.running=not self.running
  if self.running:self.acquisition.resume()
  else:self.acquisition.pause()
  self.run.setText("Pauze" if self.running else "Start")
 def single(self):
  if self.capture.source=="import":
   self.statusBar().showMessage("Single is niet beschikbaar voor een opgeslagen opname.");return
  self.running=False;self.run.setText("Start");self.acquisition.single()
 def frame(self):
  capture=self.acquisition.latest()
  if capture is not None:
   if self.canvas.decode_result is not None:
    self.canvas.decode_result=None;self.analysis_result.setText("Nieuwe opname: voer de analyse opnieuw uit.")
   self.capture=capture;self.canvas.capture=capture;self.canvas.update();self.refresh_metrics()
  status=self.acquisition.status()
  if status.error:
   self.running=False;self.run.setText("Start")
   self.statusBar().showMessage("Acquisitiefout: "+status.error)
  elif self.capture.source!="import":
   self.statusBar().showMessage(f"Simulator: {status.state} | Frames {status.produced} | Previewbuffer overgelopen: {status.overflow} | Overgeslagen weergaveframes: {status.preview_skipped}")
 def closeEvent(self,event):
  self.timer.stop()
  if not self.acquisition.close():
   event.ignore();self.statusBar().showMessage("Acquisitieworker stopt nog; sluit opnieuw na afloop van de read-timeout.");return
  super().closeEvent(event)
 def view_state(self):
  c=self.canvas
  return ViewState(c.time_div,c.pan,tuple(c.scales),tuple(c.offsets),tuple(c.visible),tuple(c.cursors),self.decoder.currentText(),int(self.baud.currentText()),self.radix.currentText())
 def restore_view(self,view):
  self.time.blockSignals(True);self.time.setValue(view.time_div*1000);self.time.blockSignals(False)
  self.pan.blockSignals(True);self.pan.setValue(round(view.pan*1000));self.pan.blockSignals(False)
  for i in range(2):
   for widget,value,method in ((self.channel_checks[i],view.visible[i],"setChecked"),(self.channel_scales[i],str(view.scales[i]).removesuffix(".0"),"setCurrentText"),(self.channel_offsets[i],view.offsets[i],"setValue")):
    widget.blockSignals(True);getattr(widget,method)(value);widget.blockSignals(False)
  c=self.canvas;c.time_div=view.time_div;c.pan=view.pan;c.scales=list(view.scales);c.offsets=list(view.offsets);c.visible=list(view.visible);c.cursors=list(view.cursors)
  self.decoder.setCurrentText(view.decoder);self.baud.setCurrentText(str(view.baud));self.radix.setCurrentText(view.radix)
 def refresh_metrics(self):
  a=self.capture.channels[0];vpp=max(a)-min(a);rms=math.sqrt(sum(x*x for x in a)/len(a))
  dt=abs(self.canvas.cursors[1]-self.canvas.cursors[0])*self.canvas.span()
  dv=self.canvas.sample(0,self.canvas.cursors[1])-self.canvas.sample(0,self.canvas.cursors[0])
  source_label="DEMO" if self.capture.source=="simulation" else self.capture.source.upper()
  self.metrics.setText(f"{source_label} CH1 · Vpp {vpp:.3g} V · RMS {rms:.3g} V · Δt {dt*1000:.3g} ms · ΔV {dv:.3g} V\n{len(a)} samples · {self.capture.rate:g} Sa/s · Hardwaretrigger / diagnose: niet beschikbaar")
 def invalidate_decode(self):
  if self.canvas.decode_result is not None:
   self.canvas.decode_result=None;self.canvas.update();self.analysis_result.setText("Instellingen gewijzigd: analyseer de samples opnieuw.")
 def analyse(self):
  self.invalidate_decode()
  try:
   result=decode_capture(self.capture,self.decoder.currentText(),int(self.baud.currentText()))
   self.acquisition.pause();self.running=False;self.run.setText("Start")
   self.canvas.decode_result=result;self.canvas.decoder_selection=None;self.canvas.update()
   self.analysis_result.setText(result.description+"\nBron: "+self.capture.source+". Drempel 2,5 V; geen ruis-/hardwarevalidatie. Klik op een decodeblok voor sample- en tijddetails.")
  except ValueError as e:self.analysis_result.setText(str(e))
 def explain(self,title,basic,advanced):
  d=QDialog(self);d.setWindowTitle(title);l=QVBoxLayout(d);t=QLabel(basic);t.setWordWrap(True);l.addWidget(t);details=QLabel(advanced);details.setWordWrap(True);details.hide();toggle=QCheckBox("Technische uitleg");toggle.toggled.connect(details.setVisible);l.addWidget(toggle);l.addWidget(details);buttons=QDialogButtonBox(QDialogButtonBox.Close);buttons.rejected.connect(d.reject);l.addWidget(buttons);d.resize(520,240);d.exec()
 def save_capture(self):
  path,_=QFileDialog.getSaveFileName(self,"Bewaar demo-opname","Owon_NG-demo.json","Demo-opname (*.json)")
  if not path:return
  try:self.capture.save(path,self.note.toPlainText(),self.view_state())
  except (OSError,ValueError) as e:QMessageBox.warning(self,"Opslaan mislukt",str(e));return
  if not self.saved:self.history.clear()
  self.saved.append(path);self.history.addItem(path);self.statusBar().showMessage("Demo-opname opgeslagen: "+path)
 def open_history(self,item):self.read_capture(item.text())
 def open_capture(self):
  path,_=QFileDialog.getOpenFileName(self,"Open demo-opname","","Demo-opname (*.json)")
  if path:self.read_capture(path)
 def read_capture(self,path):
  try:
   c,note,view=load_recording(path)
   if c.profile not in PROFILES:raise ValueError("Onbekend profiel.")
  except (OSError,ValueError,TypeError,KeyError) as e:QMessageBox.warning(self,"Opname niet geopend",str(e));return
  self.acquisition.pause()
  self.profile.blockSignals(True);self.profile.setCurrentText(c.profile);self.profile.blockSignals(False)
  if self.nav.currentRow()!=2:self.nav.setCurrentRow(0 if PROFILES[c.profile][0]=="Automotive" else 1)
  self.canvas.decode_result=None;self.analysis_result.setText("Opname geopend. Analyseer opnieuw om decodebanen te tonen.")
  self.capture=c;self.canvas.capture=c;self.note.setPlainText(note);self.running=False;self.run.setText("Start");self.provenance.setText("IMPORTED · "+("DEMO" if c.original=="simulation" else "HARDWAREBRON"))
  self.restore_view(view);self.statusBar().showMessage("Opname geopend — oorspronkelijke samples en instellingen behouden; geen live hardware.")
  self.update_guide();self.canvas.update();self.refresh_metrics();self.pages.setCurrentIndex(0)

def main():
 app=QApplication(sys.argv);app.setStyle("Fusion");app.setStyleSheet(STYLE);window=ScopeWindow();window.show();sys.exit(app.exec())
