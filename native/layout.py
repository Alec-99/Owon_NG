"""Original Qt instrument layout; no upstream code or assets copied."""
from PySide6.QtWidgets import (QWidget,QVBoxLayout,QHBoxLayout,QLabel,QListWidget,QComboBox,QToolBar,QStyle,QTabBar,QTabWidget,QSplitter,QFormLayout,QDoubleSpinBox,QCheckBox,QScrollArea,QTextEdit,QSlider)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from native.model import PROFILES,WARNING
from native.canvas import ScopeCanvas
from native.branding import BrandImage,WORDMARK

from native.theme import STYLE

class CompactSpinBox(QDoubleSpinBox):
 def textFromValue(self,value):
  text=self.locale().toString(value,"f",self.decimals())
  return text.rstrip("0").rstrip(self.locale().decimalPoint()) if self.decimals() else text


def shell(w,button,pages,version):
 w.setWindowTitle(f"OWON NG {version} — oscilloscoop")
 w.nav=QListWidget();w.nav.addItems(pages);w.nav.hide()
 file=w.menuBar().addMenu("&Bestand")
 for name,slot,key in (("Opname openen…",w.open_capture,"Ctrl+O"),("Opname bewaren…",w.save_capture,"Ctrl+S")):
  a=QAction(name,w);a.setShortcut(key);a.triggered.connect(slot);file.addAction(a)
 file.addSeparator();file.addAction("Afsluiten",w.close)
 menu=w.menuBar().addMenu("&Werkruimte")
 for i,p in enumerate(pages):
  a=QAction(p,w);a.triggered.connect(lambda checked=False,r=i:w.nav.setCurrentRow(r));menu.addAction(a)
 help=w.menuBar().addMenu("&Help");help.addAction("Bediening en veiligheid",lambda:w.nav.setCurrentRow(7));help.addSeparator();help.addAction("Over OWON NG",w.show_about)
 bar=QToolBar("Bestand",w);bar.setMovable(False);bar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon);w.addToolBar(bar)
 w.wordmark=BrandImage(WORDMARK,154,36,trim_padding=True);bar.addWidget(w.wordmark);bar.addSeparator()
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
 w.run=button("Pauzeer",w.toggle_run);w.run.setObjectName("run");w.run.setMinimumWidth(115);w.run.setToolTip("Zet de simulatie stil om de getoonde samples te onderzoeken.")
 toolbar.addWidget(w.run);w.single_button=button("Eén opname",w.single);w.single_button.setToolTip("Maak één nieuw gesimuleerd meetframe en pauzeer.");toolbar.addWidget(w.single_button);toolbar.addSpacing(12);toolbar.addWidget(QLabel("Profiel"))
 w.profile=QComboBox();w.profile.addItems(PROFILES);w.profile.setMinimumWidth(200);w.profile.currentTextChanged.connect(w.select_profile);toolbar.addWidget(w.profile)
 toolbar.addWidget(button("Herstel voorbeeld",w.apply_preset));toolbar.addStretch()
 toolbar.addWidget(button("Bediening",lambda:w.explain("Bediening","Sleep cursors A/B; gebruik het muiswiel om in tijd te zoomen.","Links/rechts bestuurt A; Shift+links/rechts bestuurt B. Schalen veranderen de weergave, niet de opgeslagen samples.")))
 layout.addLayout(toolbar)
 flow=QHBoxLayout();w.acquisition_state=QLabel("Simulatie loopt");w.acquisition_state.setObjectName("state");flow.addWidget(w.acquisition_state);flow.addSpacing(14)
 w.flow_hint=QLabel();w.flow_hint.setObjectName("hint");w.flow_hint.setWordWrap(True);flow.addWidget(w.flow_hint,1);layout.addLayout(flow)
 main=QSplitter(Qt.Horizontal);layout.addWidget(main,1)
 left=QWidget();ll=QVBoxLayout(left);ll.setContentsMargins(0,0,0,0);ll.setSpacing(0)
 w.canvas=ScopeCanvas(w.capture);w.canvas.cursorsChanged.connect(w.refresh_metrics);ll.addWidget(w.canvas,1)
 w.metrics=QLabel();w.metrics.setObjectName("metrics");w.metrics.setWordWrap(True);ll.addWidget(w.metrics)
 panrow=QHBoxLayout();panrow.addWidget(QLabel("Tijdpositie"))
 w.pan=QSlider(Qt.Horizontal);w.pan.setAccessibleName("Tijdpositie");w.pan.setRange(0,1000);w.pan.valueChanged.connect(w.pan_changed);panrow.addWidget(w.pan);ll.addLayout(panrow)
 main.addWidget(left)
 tabs=QTabWidget();tabs.setMinimumWidth(280);tabs.setMaximumWidth(360)
 controls=QWidget();cl=QVBoxLayout(controls);form=QFormLayout();form.setVerticalSpacing(8);cl.addLayout(form)
 w.time=CompactSpinBox();w.time.setRange(.05,2000);w.time.setDecimals(6);w.time.setValue(10);w.time.setSuffix(" ms/div");w.time.valueChanged.connect(w.time_changed);w.time.setToolTip("Tijd per rastervak. Een kleinere waarde zoomt horizontaal in.");form.addRow("Tijd / vak",w.time)
 w.channel_checks=[];w.channel_scales=[];w.channel_offsets=[]
 for ch,color in enumerate(("#ad7900","#007fa8")):
  label=QLabel(f"CH{ch+1}");label.setStyleSheet(f"font-weight:bold;color:{color};padding-top:10px;");form.addRow(label)
  check=QCheckBox(f"Kanaal {ch+1} tonen");check.setChecked(True);check.toggled.connect(lambda v,c=ch:w.channel_visible(c,v));form.addRow("",check);w.channel_checks.append(check)
  scale=QComboBox();scale.addItems(["0.1","0.2","0.5","1","2","5","10"]);scale.setCurrentText("2");scale.currentTextChanged.connect(lambda v,c=ch:w.scale_changed(c,float(v)));scale.setToolTip("Volt per rastervak. Een kleinere waarde maakt de trace hoger.");form.addRow("Schaal (V/div)",scale);w.channel_scales.append(scale)
  offset=CompactSpinBox();offset.setRange(-100,100);offset.setSuffix(" V");offset.valueChanged.connect(lambda v,c=ch:w.offset_changed(c,v));offset.setToolTip("Verschuift alleen de trace; verandert geen opgeslagen samples.");form.addRow("Verschuiving",offset);w.channel_offsets.append(offset)
 unavailable=button("Trigger — niet beschikbaar",lambda:None);unavailable.setEnabled(False);unavailable.setToolTip("Triggering is nog niet geïmplementeerd.");cl.addSpacing(15);cl.addWidget(unavailable)
 cl.addWidget(button("i · Schalen en probes",lambda:w.explain("Kanaalinstellingen","V/div verandert de verticale weergave; offset verschuift de trace.","Probeverhouding, koppeling en kalibratie zijn nog niet geïmplementeerd.")));cl.addStretch()
 channel_scroll=QScrollArea();channel_scroll.setWidgetResizable(True);channel_scroll.setFrameShape(QScrollArea.NoFrame);channel_scroll.setWidget(controls);tabs.addTab(channel_scroll,"Kanalen")
 guidepage=QWidget();gl=QVBoxLayout(guidepage);w.guide=QLabel();w.guide.setWordWrap(True);w.guide.setTextInteractionFlags(Qt.TextSelectableByMouse);gl.addWidget(w.guide);warning=QLabel(WARNING);warning.setWordWrap(True);warning.setStyleSheet("color:#745321;");gl.addWidget(warning);gl.addStretch();gl.addWidget(button("Herstel voorbeeld",w.apply_preset))
 scroll=QScrollArea();scroll.setWidgetResizable(True);scroll.setFrameShape(QScrollArea.NoFrame);scroll.setWidget(guidepage);tabs.addTab(scroll,"Testhulp");main.addWidget(tabs);main.setSizes([1060,290])
 bottom=QTabWidget();bottom.setMaximumHeight(155);bottom.setMinimumHeight(125)
 decoder=QWidget();dl=QVBoxLayout(decoder);ar=QHBoxLayout();ar.addWidget(QLabel("Protocol"))
 w.decoder=QComboBox();w.decoder.addItems(["PWM","UART 8N1","I²C","SPI (gepland)","CAN-protocol (gepland)"]);ar.addWidget(w.decoder)
 w.baud_label=QLabel("Baud");ar.addWidget(w.baud_label);w.baud=QComboBox();w.baud.addItems(["9600","19200","38400","115200"]);ar.addWidget(w.baud);w.radix_label=QLabel("Getallen");ar.addWidget(w.radix_label);w.radix=QComboBox();w.radix.addItems(["Hex","Dec","ASCII","Bin"]);w.radix.currentTextChanged.connect(w.canvas.set_decode_radix);ar.addWidget(w.radix);w.analyse_button=button("Analyseer signaal",w.analyse);w.analyse_button.setObjectName("analyse");w.analyse_button.setToolTip("Pauzeert de simulatie en toont het resultaat onder de trace.");ar.addWidget(w.analyse_button);ar.addStretch();dl.addLayout(ar)
 w.analysis_result=QLabel("Kies protocol en instellingen. Vaste drempel: 2,5 V. UART 8N1; I²C CH1=SCL / CH2=SDA. Niet hardware-gevalideerd.");w.analysis_result.setWordWrap(True);dl.addWidget(w.analysis_result);dl.addStretch()
 w.decoder.currentTextChanged.connect(w.invalidate_decode);w.baud.currentTextChanged.connect(w.invalidate_decode)
 w.decoder.currentTextChanged.connect(w.update_decoder_controls);w.update_decoder_controls()
 bottom.addTab(decoder,"Decoders")
 w.note=QTextEdit();w.note.setPlaceholderText("Omstandigheden, observaties en vervolgcontroles…");bottom.addTab(w.note,"Notities");layout.addWidget(bottom)
 w.update_guide();return panel
