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
 "PWM": ("Elektronica", 12000, "PWM • illustratie van pulsbreedtemodulatie", "Controleer voedingsspanning, meetbereik en probeclassificatie vóór een echte aansluiting."),
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
  elif profile == "PWM":
   a.append(5 if t * 100 % 1 < .42 else 0); b.append(2.5)
  elif profile == "CAN fysiek":
   bit = int(t * 1000) % 7 in (0, 2, 3, 6)
   a.append(3.5 if bit else 2.5); b.append(1.5 if bit else 2.5)
  elif profile == "Injector":
   a.append(5 if t * 30 % 1 < .2 else 0); b.append(0)
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
