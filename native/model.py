"""Synthetic fixtures and a bounded, versioned demo recording format."""
from dataclasses import dataclass
import math
import json
from pathlib import Path

PROFILES = {
 "CKP inductief": ("Automotive", 12000, "Krukaspositie • schematische ontbrekende tanden", "Gebruik voertuigdocumentatie om de juiste meetpunten te bepalen. Dit is geen voertuigspecifieke aansluitprocedure."),
 "Lambda narrowband": ("Automotive", 200, "Narrowband-lambdasensor • illustratief pendelsignaal", "Narrowband en wideband zijn verschillende systemen. Dit profiel is uitsluitend narrowband."),
 "Injector": ("Automotive", 12000, "Injector • schematische laagspanningsillustratie", "Live meting niet vrijgegeven: injector-flyback vereist gevalideerde, voldoende bemeten probes en een veilige procedure."),
 "CAN fysiek": ("Automotive", 12000, "CAN-H/L • fysieke spanningsillustratie, geen decoder", "Beide kanaalmassa’s uitsluitend op hetzelfde massapunt. Dit vereenvoudigde patroon is geen geldige CAN-framecapture."),
 "PWM-solenoïde": ("Automotive", 12000, "PWM-actuator • passieve spanningsillustratie", "Geen actuator aansturen vanuit de app. Controleer flyback, stroom, probeclassificatie en een voertuigspecifieke veilige procedure vóór live meting."),
 "PWM": ("Elektronica", 12000, "PWM • illustratie van pulsbreedtemodulatie", "Controleer voedingsspanning, meetbereik en probeclassificatie vóór een echte aansluiting."),
 "UART 8N1": ("Elektronica", 200000, "UART • 9600 baud, 8N1, bytes 55/A5", "Controleer logicaniveaus en gemeenschappelijke massa. Dit is geen RS-232 of differentiële aansluiting."),
 "I²C": ("Elektronica", 200000, "I²C • CH1 SCL / CH2 SDA", "Open-drain signalen vereisen passende pull-ups. Controleer busspanning en probe-invloed."),
 "Sinus": ("Elektronica", 12000, "Sinus • synthetische testbron", "Gebruik alleen meetapparatuur met geschikte spannings- en veiligheidsclassificatie."),
}
WARNING = "CH1 en CH2 delen een gemeenschappelijke massa. Verbind aardklemmen nooit met verschillende potentialen. USB-isolatie maakt de kanalen niet onderling geïsoleerd. Geen live hoogspanning-, ontsteking-, net- of EV-meting zonder gevalideerde accessoires en procedure."

@dataclass
class Capture:
 profile: str
 rate: float
 channels: list
 source: str = "simulation"
 original: str = "simulation"
 def save(self, path, note):
  Path(path).write_text(json.dumps(dict(schema=1, source=self.source, original=self.original, profile=self.profile, rate=self.rate, channels=self.channels, note=note)), encoding="utf8")

def fixture(profile, phase=0.0, n=4096):
 rate = PROFILES[profile][1]
 a, b = [], []
 for i in range(n):
  t = i / rate + phase
  if profile == "CKP inductief":
   a.append(3 * math.sin(t * 2 * math.pi * 120) if int(t * 120) % 60 < 58 else 0)
   b.append(2.5 if t * 2 % 1 < .5 else 0)
  elif profile == "Lambda narrowband":
   a.append(.45 + .35 * math.sin(t * 2 * math.pi * .7)); b.append(.45)
  elif profile in ("PWM","PWM-solenoïde"):
   a.append(5 if t * 100 % 1 < .42 else 0); b.append(2.5)
  elif profile == "CAN fysiek":
   bit = int(t * 1000) % 7 in (0, 2, 3, 6)
   a.append(3.5 if bit else 2.5); b.append(1.5 if bit else 2.5)
  elif profile == "Injector":
   a.append(5 if t * 30 % 1 < .2 else 0); b.append(0)
  elif profile == "UART 8N1":
   bit=int(t*9600)%24
   value=0x55 if int(t*9600)//24%2==0 else 0xA5
   level=True if bit<2 or bit>=12 else False if bit==2 else bool(value & (1<<(bit-3))) if bit<11 else True
   a.append(5 if level else 0);b.append(0)
  elif profile == "I²C":
   tick=i%1000
   if tick<40 or tick>=820:
    a.append(5);b.append(5 if tick<20 or tick>=840 else 0)
   elif tick<60:
    a.append(5);b.append(0)
   elif tick<780:
    half=(tick-60)//20;bit=half//2;value=0xA0 if bit<9 else 0x55;pos=bit%9
    a.append(0 if half%2==0 else 5);b.append(0 if pos==8 else 5 if value&(1<<(7-pos)) else 0)
   else:a.append(0 if tick<800 else 5);b.append(0)
  else:
   a.append(3 * math.sin(t * 2 * math.pi * 50)); b.append(math.sin(t * 2 * math.pi * 50 + .7))
 return Capture(profile, rate, [a,b])

def load(path):
 if Path(path).stat().st_size > 8_000_000: raise ValueError("Bestand is te groot (maximaal 8 MB).")
 d = json.loads(Path(path).read_text(encoding="utf8"))
 if not isinstance(d,dict): raise ValueError("Geen opnameobject.")
 if d.get("schema") != 1 or d.get("source") not in ("simulation","import"): raise ValueError("Geen ondersteunde demo-opname.")
 if d.get("profile") not in PROFILES: raise ValueError("Onbekend profiel.")
 rate=d.get("rate")
 if isinstance(rate,bool) or not isinstance(rate,(int,float)) or not math.isfinite(rate) or not 1 <= rate <= 1e8: raise ValueError("Ongeldige samplefrequentie.")
 channels=d.get("channels")
 if not isinstance(channels,list) or len(channels)!=2: raise ValueError("Twee kanalen vereist.")
 for c in channels:
  if not isinstance(c,list) or not 2<=len(c)<=100000 or any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or abs(v)>1e6 for v in c): raise ValueError("Ongeldige samples.")
 if len(channels[0])!=len(channels[1]): raise ValueError("Kanalen hebben verschillende lengtes.")
 note=d.get("note","")
 if not isinstance(note,str): raise ValueError("Ongeldige notitie.")
 return Capture(d["profile"],rate,channels,"import","simulation"), note[:20000]
