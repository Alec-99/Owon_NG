"""Immutable voltage frames; sample time is independent of UI/host scheduling."""
from dataclasses import dataclass, field
import math
import time
import uuid

MAX_SAMPLES = 1_000_000

def finite(value, name, minimum=None, maximum=None):
    try:
        valid = type(value) in (int, float) and math.isfinite(value)
    except OverflowError:
        valid = False
    if not valid:
        raise ValueError(f"Ongeldige {name}.")
    if (minimum is not None and value < minimum) or (maximum is not None and value > maximum):
        raise ValueError(f"Ongeldige {name}.")
    return value

def integer(value, name):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"Ongeldige {name}.")

@dataclass(frozen=True)
class ChannelConfig:
    channel_id: str
    unit: str = "V"
    probe_ratio: float | None = None
    coupling: str | None = None
    calibrated: bool = False

    def __post_init__(self):
        if self.channel_id not in ("CH1", "CH2") or self.unit != "V":
            raise ValueError("Alleen CH1/CH2 met voltagesamples worden ondersteund.")
        if self.probe_ratio is not None:
            finite(self.probe_ratio, "probeverhouding", 0.001, 1e6)
        if self.coupling not in (None, "AC", "DC") or type(self.calibrated) is not bool:
            raise ValueError("Ongeldige kanaalmetadata.")

@dataclass(frozen=True)
class Capture:
    profile: str
    rate: float
    channels: tuple
    source: str = "simulation"
    original: str = "simulation"
    sample_start: int = 0
    frame_index: int = 0
    received_at_ns: int | None = field(default_factory=time.time_ns)
    stream_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    capture_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    device_id: str = "simulated-scope"
    channel_config: tuple = field(default_factory=lambda: (ChannelConfig("CH1"), ChannelConfig("CH2")))

    def __post_init__(self):
        if not isinstance(self.profile, str) or not 1 <= len(self.profile) <= 128:
            raise ValueError("Ongeldig profiel.")
        finite(self.rate, "samplefrequentie", 1e-9, 1e12)
        if self.source not in ("simulation", "hardware", "import") or self.original not in ("simulation", "hardware"):
            raise ValueError("Ongeldige herkomst.")
        if self.source != "import" and self.source != self.original:
            raise ValueError("Herkomst en oorspronkelijke bron komen niet overeen.")
        for value in (self.sample_start, self.frame_index):
            integer(value, "tijd-/frame-index")
        if self.received_at_ns is not None:
            integer(self.received_at_ns, "ontvangsttijd")
        for value in (self.stream_id, self.capture_id, self.device_id):
            if not isinstance(value, str) or not 1 <= len(value) <= 256:
                raise ValueError("Ongeldige frame-identificatie.")
        if not isinstance(self.channels, (list, tuple)) or len(self.channels) != 2:
            raise ValueError("Twee kanalen vereist.")
        samples = []
        for channel in self.channels:
            if not isinstance(channel, (list, tuple)) or not 2 <= len(channel) <= MAX_SAMPLES:
                raise ValueError("Ongeldige samplelengte.")
            samples.append(tuple(finite(v, "sample", -1e9, 1e9) for v in channel))
        if len(samples[0]) != len(samples[1]):
            raise ValueError("Kanalen hebben verschillende lengtes.")
        configs = tuple(self.channel_config)
        if len(configs) != 2 or any(not isinstance(c, ChannelConfig) for c in configs):
            raise ValueError("Kanaalconfiguratie ontbreekt.")
        if tuple(c.channel_id for c in configs) != ("CH1", "CH2"):
            raise ValueError("Kanaalvolgorde moet CH1, CH2 zijn.")
        object.__setattr__(self, "channels", tuple(samples))
        object.__setattr__(self, "channel_config", configs)

    @property
    def sample_interval(self):
        return 1 / self.rate

    def save(self, path, note="", view=None):
        from native.recording import save_recording
        save_recording(path, self, note, view)

@dataclass(frozen=True)
class ViewState:
    time_div: float = 0.01
    pan: float = 0
    scales: tuple = (2.0, 2.0)
    offsets: tuple = (0.0, 0.0)
    visible: tuple = (True, True)
    cursors: tuple = (0.3, 0.7)
    decoder: str = "PWM"
    baud: int = 9600

    def __post_init__(self):
        finite(self.time_div, "tijdbasis", 0.00005, 2)
        finite(self.pan, "tijdpositie", 0, 1)
        for key in ("scales", "offsets", "visible", "cursors"):
            value = getattr(self, key)
            if not isinstance(value, (tuple, list)) or len(value) != 2:
                raise ValueError("Ongeldige weergave-instellingen.")
            object.__setattr__(self, key, tuple(value))
        for value in self.scales:
            if value not in (0.1, 0.2, 0.5, 1, 2, 5, 10) or type(value) is bool:
                raise ValueError("Onbekende V/div.")
        for value in self.offsets:
            finite(value, "offset", -100, 100)
        for value in self.cursors:
            finite(value, "cursor", 0, 1)
        if any(type(v) is not bool for v in self.visible):
            raise ValueError("Ongeldige kanaalzichtbaarheid.")
        if self.decoder not in ("PWM", "UART 8N1", "I²C", "SPI (gepland)", "CAN-protocol (gepland)"):
            raise ValueError("Onbekende decoder.")
        if type(self.baud) is not int or self.baud not in (9600, 19200, 38400, 115200):
            raise ValueError("Onbekende baudrate.")
