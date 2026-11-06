"""Independent sample-indexed decode events; no UI or hardware dependencies."""
from dataclasses import dataclass
import math
from statistics import median
from native.capture import finite

@dataclass(frozen=True)
class DecodeEvent:
    start: int
    stop: int
    kind: str
    value: int | None = None
    ack: bool | None = None
    text: str = ""

    def label(self, radix="Hex"):
        if self.value is None:
            return self.text
        value = self.value >> 1 if self.kind == "address" else self.value
        if radix == "ASCII":
            label = chr(value) if 32 <= value <= 126 else f"\\x{value:02X}"
        elif radix == "Dec":
            label = str(value)
        elif radix == "Bin":
            label = f"{value:08b}"
        else:
            label = f"0x{value:02X}"
        if self.kind == "address":
            label = f"Adr {label} {'R' if self.value & 1 else 'W'}"
        if self.ack is not None:
            label += " · ACK" if self.ack else " · NACK"
        return label

@dataclass(frozen=True)
class DecodeResult:
    capture_id: str
    protocol: str
    rate: float
    events: tuple
    description: str

def pwm_periods(samples, rate, threshold=2.5):
    finite(rate, "samplefrequentie", 1e-9)
    finite(threshold, "drempel")
    edges = [i for i in range(1, len(samples)) if samples[i-1] < threshold <= samples[i]]
    if len(edges) < 3:
        raise ValueError("Minimaal drie stijgende flanken vereist.")
    result = []
    for a,b in zip(edges, edges[1:]):
        if b-a < 8:
            raise ValueError("Te weinig samples per PWM-periode.")
        result.append((a,b,sum(v >= threshold for v in samples[a:b])/(b-a)))
    return result

def uart_events(samples, rate, baud=9600, threshold=2.5):
    finite(rate, "samplefrequentie", 1e-9)
    finite(baud, "baudrate", 1)
    finite(threshold, "drempel")
    spb = rate/baud
    if spb < 8:
        raise ValueError("UART vereist minimaal 8 samples per bit.")
    events = []
    i = 1
    while i < len(samples):
        if samples[i-1] >= threshold > samples[i]:
            stop_sample = round(i+9.5*spb)
            if stop_sample >= len(samples):
                events.append(DecodeEvent(i,len(samples),"incomplete",text="Onvolledig"))
                break
            if samples[round(i+.5*spb)] >= threshold:
                i += 1
                continue
            value = sum(int(samples[round(i+(1.5+b)*spb)] >= threshold) << b for b in range(8))
            stop = min(len(samples), math.ceil(i+10*spb))
            if samples[stop_sample] >= threshold:
                events.append(DecodeEvent(i,stop,"data",value))
            else:
                events.append(DecodeEvent(i,stop,"framing",text="Framingfout"))
            i = max(i+1, round(i+10*spb))
        else:
            i += 1
    return tuple(events)

def i2c_events(clock, data, rate, threshold=2.5):
    finite(rate,"samplefrequentie",1e-9)
    finite(threshold,"drempel")
    if len(clock) != len(data):
        raise ValueError("SCL en SDA moeten even lang zijn.")
    active = False
    address = True
    bits = []
    events = []
    byte_start = 0
    for i in range(1,len(clock)):
        scl,old_scl = clock[i] >= threshold, clock[i-1] >= threshold
        sda,old_sda = data[i] >= threshold, data[i-1] >= threshold
        if scl and old_scl and sda != old_sda:
            if bits:
                events.append(DecodeEvent(byte_start,i,"incomplete",text="Onvolledig"))
            if not sda:
                events.append(DecodeEvent(i,i+1,"start",text="START"))
                active, address = True, True
            else:
                if active:
                    events.append(DecodeEvent(i,i+1,"stop",text="STOP"))
                active = False
            bits = []
        elif active and scl and not old_scl:
            if not bits:
                byte_start = i
            bits.append(sda)
            if len(bits) == 9:
                value = sum(int(bit) << (7-n) for n,bit in enumerate(bits[:8]))
                kind = "address" if address and value & 0xF8 != 0xF0 else "data"
                events.append(DecodeEvent(byte_start,i+1,kind,value,not bits[8]))
                address = False
                bits = []
    if bits:
        events.append(DecodeEvent(byte_start,len(clock),"incomplete",text="Onvolledig"))
    return tuple(events)

def decode_capture(capture, protocol, baud=9600, threshold=2.5):
    if protocol == "PWM":
        periods = pwm_periods(capture.channels[0],capture.rate,threshold)
        freq = 1/median((b-a)/capture.rate for a,b,_ in periods)
        duty = 100*median(v for _,_,v in periods)
        events = tuple(DecodeEvent(a,b,"pwm",text=f"{v*100:.3g}%") for a,b,v in periods)
        description = f"PWM: {freq:.4g} Hz · duty {duty:.3g}%"
    elif protocol == "UART 8N1":
        events = uart_events(capture.channels[0],capture.rate,baud,threshold)
        description = f"UART 8N1 · {baud} baud · {sum(e.kind=='data' for e in events)} bytes · {sum(e.kind=='framing' for e in events)} framingfouten"
    elif protocol == "I²C":
        events = i2c_events(*capture.channels,capture.rate,threshold)
        description = f"I²C · {sum(e.kind=='start' for e in events)} START · {sum(e.value is not None for e in events)} bytes · {sum(e.ack is True for e in events)} ACK · {sum(e.ack is False for e in events)} NACK"
    else:
        raise ValueError("Deze decoder is nog niet beschikbaar.")
    partial = sum(e.kind=="incomplete" for e in events)
    if partial:
        description += f" · {partial} onvolledige velden"
    return DecodeResult(capture.capture_id,protocol,capture.rate,events,description)
