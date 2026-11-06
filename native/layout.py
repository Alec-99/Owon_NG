"""Original Qt instrument layout; no upstream code or assets copied."""
from PySide6.QtWidgets import (QWidget,QVBoxLayout,QHBoxLayout,QLabel,QListWidget,QComboBox,QToolBar,QStyle,QTabBar,QTabWidget,QSplitter,QFormLayout,QDoubleSpinBox,QCheckBox,QScrollArea,QTextEdit,QSlider)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from native.model import PROFILES,WARNING
from native.canvas import ScopeCanvas

STYLE="""
QWidget {font-family:'Segoe UI';font-size:12px;color:#26313a;}
QMainWindow,QToolBar,QMenuBar {background:#edf0f2;}
QToolBar {border:0;border-bottom:1px solid #c4cbd0;spacing:5px;padding:4px;}
QPushButton,QComboBox,QDoubleSpinBox {min-height:23px;}
QPushButton {padding:2px 9px;}
QTabWidget::pane {border:1px solid #c2c9ce;background:#f5f6f7;}
QTabBar::tab {padding:6px 15px;}
QTextEdit {background:#fff;border:1px solid #c2c9ce;}
QListWidget {background:white;}
QLabel#source {color:#805500;background:#f6e9c7;padding:4px 9px;font-weight:600;}
QLabel#safety {background:#fff5db;color:#5a4723;border-bottom:1px solid #dfd0a8;padding:5px 10px;}
QLabel#metrics {font-family:Consolas,'DejaVu Sans Mono';font-size:12px;background:#e6ebef;padding:7px;color:#243746;}
QSplitter::handle {background:#d6dde2;}
"""

def shell(w,button,pages,version):
 w.setWindowTitle(f"Owon NG {version} — oscilloscoop")
 w.nav=QListWidget();w.nav.addItems(pages);w.nav.hide()
 file=w.menuBar().addMenu("&Bestand")
 for name,slot,key in (("Opname openen…",w.open_capture,"Ctrl+O"),("Opname bewaren…",w.save_capture,"Ctrl+S")):
  a=QAction(name,w);a.setShortcut(key);a.triggered.connect(slot);file.addAction(a)
 file.addSeparator();file.addAction("Afsluiten",w.close)
 menu=w.menuBar().addMenu("&Werkruimte")
 for i,p in enumerate(pages):
  a=QAction(p,w);a.triggered.connect(lambda checked=False,r=i:w.nav.setCurrentRow(r));menu.addAction(a)
 help=w.menuBar().addMenu("&Help");help.addAction("Bediening en veiligheid",lambda:w.nav.setCurrentRow(7))
 bar=QToolBar("Bestand",w);bar.setMovable(False);w.addToolBar(bar)
 for text,slot,icon in (("Openen",w.open_capture,QStyle.SP_DialogOpenButton),("Bewaren",w.save_capture,QStyle.SP_DialogSaveButton)):
  a=QAction(w.style().standardIcon(icon),text,w);a.triggered.connect(slot);bar.addAction(a)
 bar.addSeparator();bar.addWidget(QLabel("  Werkruimte  "))
 w.modes=QComboBox();w.modes.addItems(pages[:3]);w.modes.setMinimumWidth(145);w.modes.currentIndexChanged.connect(w.nav.setCurrentRow);bar.addWidget(w.modes)
 spacer=QWidget();from PySide6.QtWidgets import QSizePolicy
 spacer.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred);bar.addWidget(spacer)
 w.provenance=QLabel("DEMO · GESIMULEERD");w.provenance.setObjectName("source");bar.addWidget(w.provenance)
 root=QWidget();w.setCentralWidget(root);content=QVBoxLayout(root);content.setContentsMargins(0,0,0,0);content.setSpacing(0)
 w.safety=QLabel("CH1 en CH2 delen één massa. Aardklemmen uitsluitend op hetzelfde potentiaal. Geen live hoogspanning zonder gevalideerde procedure.")
 w.safety.setObjectName("safety");w.safety.setWordWrap(True);w.safety.setToolTip(WARNING);content.addWidget(w.safety)
 return content

def scope(w,button):
 panel=QWidget();layout=QVBoxLayout(panel);layout.setContentsMargins(6,6,6,4);layout.setSpacing(5)
 toolbar=QHBoxLayout()
 w.run=button("Pauze",w.toggle_run);w.run.setMinimumWidth(74);w.run.setStyleSheet("color:#155c40;font-weight:600;")
 toolbar.addWidget(w.run);toolbar.addWidget(button("Single",w.single));toolbar.addSpacing(12);toolbar.addWidget(QLabel("Profiel"))
 w.profile=QComboBox();w.profile.addItems(PROFILES);w.profile.setMinimumWidth(200);w.profile.currentTextChanged.connect(w.select_profile);toolbar.addWidget(w.profile)
 toolbar.addWidget(button("Preset toepassen",w.apply_preset));toolbar.addStretch()
 toolbar.addWidget(button("i",lambda:w.explain("Bediening","Sleep cursors A/B; gebruik het muiswiel om in tijd te zoomen.","Links/rechts bestuurt A; Shift+links/rechts bestuurt B. Schalen veranderen de weergave, niet de opgeslagen samples.")))
 layout.addLayout(toolbar)
 main=QSplitter(Qt.Horizontal);layout.addWidget(main,1)
 left=QWidget();ll=QVBoxLayout(left);ll.setContentsMargins(0,0,0,0);ll.setSpacing(0)
 w.canvas=ScopeCanvas(w.capture);w.canvas.cursorsChanged.connect(w.refresh_metrics);ll.addWidget(w.canvas,1)
 w.metrics=QLabel();w.metrics.setObjectName("metrics");w.metrics.setWordWrap(True);ll.addWidget(w.metrics)
 panrow=QHBoxLayout();panrow.addWidget(QLabel("Tijdpositie"))
 w.pan=QSlider(Qt.Horizontal);w.pan.setAccessibleName("Tijdpositie");w.pan.setRange(0,1000);w.pan.valueChanged.connect(w.pan_changed);panrow.addWidget(w.pan);ll.addLayout(panrow)
 main.addWidget(left)
 tabs=QTabWidget();tabs.setMinimumWidth(280);tabs.setMaximumWidth(360)
 controls=QWidget();cl=QVBoxLayout(controls);form=QFormLayout();form.setVerticalSpacing(8);cl.addLayout(form)
 w.time=QDoubleSpinBox();w.time.setRange(.05,2000);w.time.setDecimals(6);w.time.setValue(10);w.time.setSuffix(" ms/div");w.time.valueChanged.connect(w.time_changed);form.addRow("Tijdbasis",w.time)
 w.channel_checks=[];w.channel_scales=[];w.channel_offsets=[]
 for ch,color in enumerate(("#ad7900","#007fa8")):
  label=QLabel(f"CH{ch+1}");label.setStyleSheet(f"font-weight:bold;color:{color};padding-top:10px;");form.addRow(label)
  check=QCheckBox("Zichtbaar");check.setChecked(True);check.toggled.connect(lambda v,c=ch:w.channel_visible(c,v));form.addRow("",check);w.channel_checks.append(check)
  scale=QComboBox();scale.addItems(["0.1","0.2","0.5","1","2","5","10"]);scale.setCurrentText("2");scale.currentTextChanged.connect(lambda v,c=ch:w.scale_changed(c,float(v)));form.addRow("V/div",scale);w.channel_scales.append(scale)
  offset=QDoubleSpinBox();offset.setRange(-100,100);offset.setSuffix(" V");offset.valueChanged.connect(lambda v,c=ch:w.offset_changed(c,v));form.addRow("Offset",offset);w.channel_offsets.append(offset)
 unavailable=button("Trigger — niet beschikbaar",lambda:None);unavailable.setEnabled(False);unavailable.setToolTip("Triggering is nog niet geïmplementeerd.");cl.addSpacing(15);cl.addWidget(unavailable)
 cl.addWidget(button("i · Schalen en probes",lambda:w.explain("Kanaalinstellingen","V/div verandert de verticale weergave; offset verschuift de trace.","Probeverhouding, koppeling en kalibratie zijn nog niet geïmplementeerd.")));cl.addStretch()
 tabs.addTab(controls,"Kanalen")
 guidepage=QWidget();gl=QVBoxLayout(guidepage);w.guide=QLabel();w.guide.setWordWrap(True);w.guide.setTextInteractionFlags(Qt.TextSelectableByMouse);gl.addWidget(w.guide);warning=QLabel(WARNING);warning.setWordWrap(True);warning.setStyleSheet("color:#745321;");gl.addWidget(warning);gl.addStretch();gl.addWidget(button("Preset toepassen",w.apply_preset))
 scroll=QScrollArea();scroll.setWidgetResizable(True);scroll.setFrameShape(QScrollArea.NoFrame);scroll.setWidget(guidepage);tabs.addTab(scroll,"Testhulp");main.addWidget(tabs);main.setSizes([1060,290])
 bottom=QTabWidget();bottom.setMaximumHeight(155);bottom.setMinimumHeight(125)
 decoder=QWidget();dl=QVBoxLayout(decoder);ar=QHBoxLayout();ar.addWidget(QLabel("Protocol"))
 w.decoder=QComboBox();w.decoder.addItems(["PWM","UART 8N1","I²C","SPI (gepland)","CAN-protocol (gepland)"]);ar.addWidget(w.decoder)
 ar.addWidget(QLabel("Baud"));w.baud=QComboBox();w.baud.addItems(["9600","19200","38400","115200"]);ar.addWidget(w.baud);ar.addWidget(QLabel("Weergave"));w.radix=QComboBox();w.radix.addItems(["Hex","Dec","ASCII","Bin"]);w.radix.currentTextChanged.connect(w.canvas.set_decode_radix);ar.addWidget(w.radix);ar.addWidget(button("Analyseer",w.analyse));ar.addStretch();dl.addLayout(ar)
 w.analysis_result=QLabel("Kies protocol en instellingen. Vaste drempel: 2,5 V. UART 8N1; I²C CH1=SCL / CH2=SDA. Niet hardware-gevalideerd.");w.analysis_result.setWordWrap(True);dl.addWidget(w.analysis_result);dl.addStretch()
 w.decoder.currentTextChanged.connect(w.invalidate_decode);w.baud.currentTextChanged.connect(w.invalidate_decode)
 w.baud.setEnabled(False);w.decoder.currentTextChanged.connect(lambda name:w.baud.setEnabled(name=="UART 8N1"))
 bottom.addTab(decoder,"Decoders")
 w.note=QTextEdit();w.note.setPlaceholderText("Omstandigheden, observaties en vervolgcontroles…");bottom.addTab(w.note,"Notities");layout.addWidget(bottom)
 w.update_guide();return panel
