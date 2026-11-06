import sys, math, json
from pathlib import Path
from PySide6.QtWidgets import (QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QListWidget,QStackedWidget,QLabel,QPushButton,QComboBox,QDoubleSpinBox,QCheckBox,QSlider,QTextEdit,QFileDialog,QMessageBox,QGroupBox,QFormLayout,QSplitter,QDialog,QDialogButtonBox,QScrollArea)
from PySide6.QtCore import Qt,QTimer
from native.model import PROFILES,WARNING,fixture,load
from native.canvas import ScopeCanvas

VERSION="0.3.0"
PAGES=["Automotive","Elektronica","Vrij meten","Bibliotheek","Opnames / Geschiedenis","Rapporten","Instellingen","Help"]
STYLE="""
QWidget{background:#121d26;color:#e4eef5;font:14px 'Segoe UI';}
QMainWindow{background:#101820} QGroupBox{border:1px solid #334957;border-radius:8px;margin-top:14px;padding:15px} QGroupBox::title{subcontrol-origin:margin;left:12px;color:#8cd2dc}
QPushButton,QComboBox,QDoubleSpinBox{background:#243744;border:1px solid #496071;border-radius:5px;padding:7px} QPushButton:hover{background:#335568} QPushButton:disabled{color:#8b99a2}
QListWidget{border:0;background:#182632;min-width:160px} QListWidget::item{padding:12px} QListWidget::item:selected{background:#315666}
QTextEdit{background:#0e1921;border:1px solid #3b5362;border-radius:5px;padding:8px}
"""
def button(text,fn):
 b=QPushButton(text);b.clicked.connect(fn);return b
def group(title):
 g=QGroupBox(title);l=QVBoxLayout(g);return g,l

class ScopeWindow(QMainWindow):
 def __init__(self):
  super().__init__()
  self.setWindowTitle(f"Owon NG {VERSION} — native oscilloscoop · DEMO")
  self.resize(1440,960);self.phase=0.;self.running=True;self.saved=[];self.capture=fixture("CKP inductief")
  root=QWidget();self.setCentralWidget(root);outer=QHBoxLayout(root)
  self.nav=QListWidget();self.nav.addItems(PAGES);self.nav.setMaximumWidth(220);outer.addWidget(self.nav)
  content=QVBoxLayout();outer.addLayout(content,1)
  top=QHBoxLayout();top.addWidget(QLabel(f"<h2>OWON NG <small>{VERSION}</small></h2>"));top.addStretch()
  self.provenance=QLabel("DEMO · GESIMULEERD — geen hardware");top.addWidget(self.provenance)
  top.addWidget(button("Open opname",self.open_capture));top.addWidget(button("Bewaar opname",self.save_capture));content.addLayout(top)
  self.safety=QLabel(WARNING);self.safety.setWordWrap(True);self.safety.setStyleSheet("background:#36291d;color:#f6d5a7;padding:12px;border-radius:5px;");content.addWidget(self.safety)
  self.pages=QStackedWidget();content.addWidget(self.pages,1)
  self.scope=self.make_scope();self.pages.addWidget(self.scope)
  self.library=self.make_library();self.pages.addWidget(self.library)
  self.history=QListWidget();self.history.addItem("Nog geen lokaal opgeslagen opnames.");self.history.itemDoubleClicked.connect(self.open_history);self.pages.addWidget(self.history)
  self.report=QTextEdit();self.report.setReadOnly(True);self.pages.addWidget(self.report)
  settings=QLabel("Hardware niet verbonden.\nUSB, decoders en gevalideerde diagnostiek worden later toegevoegd.\n\nDeze app toont uitsluitend synthetische fixtures en geïmporteerde demo-opnames.");settings.setWordWrap(True);self.pages.addWidget(settings)
  help_page=QTextEdit();help_page.setReadOnly(True);help_page.setPlainText("Bediening\n\nStart/Pauze bestuurt de simulatie. Single maakt één nieuwe demo-frame.\nSleep cursors A/B in de grafiek; links/rechts bestuurt cursor A, Shift+links/rechts cursor B. Het muiswiel zoomt in tijd.\n\nV/div verandert de weergave, niet de samples. Tijdzoom en verschuiving houden de sampletijd intact.\n\nBewaar/Open gebruikt een versiegebonden JSON-bestand met herkomst en notitie.\n\n"+WARNING);self.pages.addWidget(help_page)
  self.nav.currentRowChanged.connect(self.navigate);self.nav.setCurrentRow(0)
  self.timer=QTimer(self);self.timer.timeout.connect(self.frame);self.timer.start(100)
  self.statusBar().showMessage("Native Qt-interface · DEMO · geen meetinstrument of foutdiagnose")
  self.refresh_metrics()
 def make_scope(self):
  w=QWidget();layout=QVBoxLayout(w)
  toolbar=QHBoxLayout()
  self.profile=QComboBox();self.profile.addItems(PROFILES);self.profile.currentTextChanged.connect(self.select_profile);toolbar.addWidget(self.profile,1)
  self.run=button("Ⅱ Pauze",self.toggle_run);toolbar.addWidget(self.run);toolbar.addWidget(button("Single",self.single))
  toolbar.addWidget(button("i · Bediening",lambda:self.explain("Scopebediening","De signalen worden synthetisch gegenereerd. Pauzeren houdt het huidige frame vast.","Een frame bevat 4096 samples met een expliciete samplefrequentie. De tijdbasis bepaalt alleen het zichtbare tijdvenster.")))
  layout.addLayout(toolbar)
  split=QSplitter(Qt.Horizontal);layout.addWidget(split,1)
  left=QWidget();ll=QVBoxLayout(left);self.canvas=ScopeCanvas(self.capture);self.canvas.cursorsChanged.connect(self.refresh_metrics);ll.addWidget(self.canvas,1)
  self.metrics=QLabel();self.metrics.setWordWrap(True);ll.addWidget(self.metrics)
  self.pan=QSlider(Qt.Horizontal);self.pan.setAccessibleName("Tijdvenster verschuiven");self.pan.setRange(0,1000);self.pan.valueChanged.connect(self.pan_changed);ll.addWidget(QLabel("Tijdvenster verschuiven"));ll.addWidget(self.pan);split.addWidget(left)
  side=QWidget();sl=QVBoxLayout(side);side.setMinimumWidth(270)
  g,gl=group("Weergave");form=QFormLayout();gl.addLayout(form)
  self.time=QDoubleSpinBox();self.time.setRange(.05,2000);self.time.setDecimals(2);self.time.setValue(10);self.time.setSuffix(" ms/div");self.time.valueChanged.connect(self.time_changed);form.addRow("Tijdbasis",self.time)
  for ch in range(2):
   row=QHBoxLayout();check=QCheckBox(f"CH{ch+1}");check.setChecked(True);check.toggled.connect(lambda v,c=ch:self.channel_visible(c,v));row.addWidget(check)
   scale=QComboBox();scale.addItems(["0.1","0.2","0.5","1","2","5","10"]);scale.setCurrentText("2");scale.currentTextChanged.connect(lambda v,c=ch:self.scale_changed(c,float(v)));row.addWidget(scale);form.addRow("V/div",row)
   offset=QDoubleSpinBox();offset.setRange(-100,100);offset.setSuffix(" V");offset.valueChanged.connect(lambda v,c=ch:self.offset_changed(c,v));form.addRow(f"CH{ch+1} offset",offset)
  unavailable=button("Trigger · nog niet beschikbaar",lambda:None);unavailable.setEnabled(False);unavailable.setToolTip("Hardwaretrigger en triggeralgoritmes zijn niet geïmplementeerd.");gl.addWidget(unavailable)
  gl.addWidget(button("i · Schalen en probes",lambda:self.explain("Schalen","V/div bepaalt hoeveel volt één rastervak vertegenwoordigt. Dit verandert geen opgeslagen samples.","Probeverhoudingen, AC/DC-koppeling en kalibratie zijn niet beschikbaar. Er is geen echte probe aangesloten.")));sl.addWidget(g)
  g,gl=group("Begeleide test");self.guide=QLabel();self.guide.setWordWrap(True);gl.addWidget(self.guide);gl.addWidget(button("Pas demo-preset toe",self.apply_preset));sl.addWidget(g)
  g,gl=group("Observatie");self.note=QTextEdit();self.note.setPlaceholderText("Noteer omstandigheden en observaties…");gl.addWidget(self.note);sl.addWidget(g,1);scroll=QScrollArea();scroll.setWidgetResizable(True);scroll.setWidget(side);scroll.setMinimumWidth(300);split.addWidget(scroll);split.setSizes([900,340])
  self.update_guide();return w
 def make_library(self):
  w=QWidget();l=QVBoxLayout(w);l.addWidget(QLabel("<h2>Illustratieve testprofielen</h2>Geen bekende-goede voertuigmetingen."))
  for name,(_,_,desc,safety) in PROFILES.items():
   l.addWidget(button(name+" — "+desc,lambda checked=False,n=name:self.choose_from_library(n)))
  l.addStretch();return w
 def choose_from_library(self,name):
  self.nav.setCurrentRow(0 if PROFILES[name][0]=="Automotive" else 1);self.profile.setCurrentText(name)
 def navigate(self,row):
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
  self.capture=fixture(name);self.canvas.capture=self.capture;self.provenance.setText("DEMO · GESIMULEERD — geen hardware");self.canvas.update();self.update_guide();self.refresh_metrics()
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
   self.explain("Geïmporteerde opname","Deze opname blijft onveranderd. Kies een demo-profiel om nieuwe signalen te simuleren.","Import wijzigt de samplefrequentie en oorspronkelijke samples niet.");return
  self.running=not self.running;self.run.setText("Ⅱ Pauze" if self.running else "▶ Start")
 def single(self):
  if self.capture.source=="import":return
  self.running=False;self.run.setText("▶ Start");self.next_frame()
 def frame(self):
  if self.running and self.capture.source=="simulation":self.next_frame()
 def next_frame(self):
  self.phase+=.1;self.capture=fixture(self.profile.currentText(),self.phase);self.canvas.capture=self.capture;self.canvas.update();self.refresh_metrics()
 def refresh_metrics(self):
  a=self.capture.channels[0];vpp=max(a)-min(a);rms=math.sqrt(sum(x*x for x in a)/len(a))
  dt=abs(self.canvas.cursors[1]-self.canvas.cursors[0])*self.canvas.span()
  dv=self.canvas.sample(0,self.canvas.cursors[1])-self.canvas.sample(0,self.canvas.cursors[0])
  self.metrics.setText(f"DEMO CH1 · Vpp {vpp:.3g} V · RMS {rms:.3g} V · Δt {dt*1000:.3g} ms · ΔV {dv:.3g} V\n{len(a)} samples · {self.capture.rate:g} Sa/s · Trigger/decoders/diagnose: niet beschikbaar")
 def explain(self,title,basic,advanced):
  d=QDialog(self);d.setWindowTitle(title);l=QVBoxLayout(d);t=QLabel(basic);t.setWordWrap(True);l.addWidget(t);details=QLabel(advanced);details.setWordWrap(True);details.hide();toggle=QCheckBox("Technische uitleg");toggle.toggled.connect(details.setVisible);l.addWidget(toggle);l.addWidget(details);buttons=QDialogButtonBox(QDialogButtonBox.Close);buttons.rejected.connect(d.reject);l.addWidget(buttons);d.resize(520,240);d.exec()
 def save_capture(self):
  path,_=QFileDialog.getSaveFileName(self,"Bewaar demo-opname","Owon_NG-demo.json","Demo-opname (*.json)")
  if not path:return
  try:self.capture.save(path,self.note.toPlainText())
  except OSError as e:QMessageBox.warning(self,"Opslaan mislukt",str(e));return
  if not self.saved:self.history.clear()
  self.saved.append(path);self.history.addItem(path);self.statusBar().showMessage("Demo-opname opgeslagen: "+path)
 def open_history(self,item):self.read_capture(item.text())
 def open_capture(self):
  path,_=QFileDialog.getOpenFileName(self,"Open demo-opname","","Demo-opname (*.json)")
  if path:self.read_capture(path)
 def read_capture(self,path):
  try:c,note=load(path)
  except (OSError,ValueError,TypeError,KeyError) as e:QMessageBox.warning(self,"Opname niet geopend",str(e));return
  self.profile.blockSignals(True);self.profile.setCurrentText(c.profile);self.profile.blockSignals(False)
  self.capture=c;self.canvas.capture=c;self.note.setPlainText(note);self.running=False;self.run.setText("▶ Start");self.provenance.setText("IMPORTED · oorspronkelijke data: SIMULATIE")
  self.update_guide();self.canvas.update();self.refresh_metrics();self.pages.setCurrentIndex(0)

def main():
 app=QApplication(sys.argv);app.setStyle("Fusion");app.setStyleSheet(STYLE);window=ScopeWindow();window.show();sys.exit(app.exec())
