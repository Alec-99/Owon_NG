"""Synthetic fixtures and a bounded, versioned demo recording format."""
from native.capture import Capture
import math

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
   tick=(i+round(phase*rate))%1000
   if tick<40 or tick>=820:
    a.append(5);b.append(5 if tick<20 or tick>=840 else 0)
   elif tick<60:
    a.append(5);b.append(0)
   elif tick<780:
    half=(tick-60)//20;bit=half//2;value=0xA0 if bit<9 else 0x55;pos=bit%9
    a.append(0 if half%2==0 else 5);b.append(0 if pos==8 else 5 if value&(1<<(7-pos)) else 0)
   else:a.append(5);b.append(0)
  else:
   a.append(3 * math.sin(t * 2 * math.pi * 50)); b.append(math.sin(t * 2 * math.pi * 50 + .7))
 return Capture(profile, rate, [a,b])

def load(path):
 from native.recording import load_recording
 capture,note,_=load_recording(path)
 if capture.profile not in PROFILES:raise ValueError("Onbekend profiel.")
 return capture,note
