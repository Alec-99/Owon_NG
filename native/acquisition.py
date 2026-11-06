"""One adapter owner thread, bounded preview queue and explicit lifecycle/errors."""
from collections import deque
from dataclasses import dataclass, replace
from queue import Queue, Empty
from threading import Event, Lock, Thread
from typing import Protocol
import time
import uuid
from native.capture import Capture, finite
from native.model import PROFILES, fixture

@dataclass(frozen=True)
class Capabilities:
    source: str
    channels: int
    hardware_verified: bool
    trigger: bool = False

class ScopeAdapter(Protocol):
    """read_frame must return/raise within its bounded timeout, never touch Qt."""
    def connect(self) -> Capabilities: ...
    def configure(self, profile: str) -> None: ...
    def read_frame(self, timeout: float) -> Capture: ...
    def disconnect(self) -> None: ...

class SimulatedScope:
    def __init__(self):
        self.connected = False
        self.configure("CKP inductief")

    def connect(self):
        self.connected = True
        return Capabilities("simulation", 2, False)

    def configure(self, profile):
        if profile not in PROFILES:
            raise ValueError("Onbekend simulatieprofiel.")
        self.profile = profile
        self.start = 0
        self.index = 0
        self.stream_id = str(uuid.uuid4())

    def read_frame(self, timeout=0.25):
        if not self.connected:
            raise RuntimeError("Simulator is niet verbonden.")
        rate = PROFILES[self.profile][1]
        frame = replace(fixture(self.profile, self.start / rate),
                        sample_start=self.start, frame_index=self.index,
                        stream_id=self.stream_id)
        self.start += len(frame.channels[0])
        self.index += 1
        return frame

    def disconnect(self):
        self.connected = False

class Vds1022Adapter:
    """Explicit boundary only. No USB commands or undocumented capabilities."""
    def connect(self):
        raise RuntimeError("OWON-adapter nog niet geïmplementeerd/gevalideerd. Zie HARDWARE_VALIDATION.md.")

    def configure(self, profile):
        raise RuntimeError("OWON-configuratie niet beschikbaar.")

    def read_frame(self, timeout=0.25):
        raise RuntimeError("OWON-acquisitie niet beschikbaar.")

    def disconnect(self):
        pass

@dataclass(frozen=True)
class AcquisitionStatus:
    state: str
    produced: int
    overflow: int
    preview_skipped: int
    error: str | None

class Acquisition:
    def __init__(self, adapter=None, capacity=8, interval=0.1, read_timeout=0.25):
        if type(capacity) is not int or capacity < 1:
            raise ValueError("Ongeldige acquisitiebuffer.")
        finite(interval,"acquisitie-interval",1e-6)
        finite(read_timeout,"read-timeout",1e-6)
        self.adapter = adapter if adapter is not None else SimulatedScope()
        self.capacity = capacity
        self.interval = interval
        self.read_timeout = read_timeout
        self._lock = Lock()
        self._commands = Queue()
        self._quit = Event()
        self._frames = deque()
        self._generation = 0
        self._requested_profile = None
        self._state = "disconnected"
        self._produced = self._overflow = self._skipped = 0
        self._error = None
        self._capabilities = None
        self._thread = Thread(target=self._work, name="scope-acquisition", daemon=True)
        self._thread.start()

    def _submit(self, kind, value=None):
        with self._lock:
            if self._quit.is_set():
                raise RuntimeError("Acquisitie is gesloten.")
            self._generation += 1
            generation = self._generation
            self._frames.clear()
            self._error = None
            if kind == "configure":
                self._requested_profile = value[0]
            self._commands.put((generation, kind, value, self._requested_profile))

    def configure(self, profile, running=True):
        self._submit("configure", (profile, running))

    def resume(self):
        self._submit("resume")

    def pause(self):
        self._submit("pause")

    def single(self):
        self._submit("single")

    def latest(self):
        with self._lock:
            if not self._frames:
                return None
            self._skipped += len(self._frames) - 1
            frame = self._frames[-1]
            self._frames.clear()
            return frame

    def status(self):
        with self._lock:
            return AcquisitionStatus(self._state, self._produced, self._overflow, self._skipped, self._error)

    def close(self, timeout=2):
        self._quit.set()
        self._commands.put((0, "close", None, None))
        self._thread.join(timeout)
        return not self._thread.is_alive()

    def _set_state(self, state, error=None, generation=None):
        with self._lock:
            if generation is not None and generation != self._generation:
                return
            self._state, self._error = state, error

    def _publish(self, generation):
        frame = self.adapter.read_frame(timeout=self.read_timeout)
        if not isinstance(frame, Capture):
            raise TypeError("Adapter gaf geen geldig meetframe terug.")
        caps = self._capabilities
        if caps is None or frame.source != caps.source or (frame.source == "hardware" and not caps.hardware_verified):
            raise RuntimeError("Adapterherkomst of hardwarevalidatie is niet bevestigd.")
        with self._lock:
            if generation != self._generation or self._quit.is_set():
                return
            if len(self._frames) == self.capacity:
                self._frames.popleft()
                self._overflow += 1
            self._frames.append(frame)
            self._produced += 1

    def _work(self):
        running = False
        connected = False
        generation = 0
        configured_profile = None
        deadline = time.monotonic()
        try:
            while not self._quit.is_set():
                timeout = max(0, deadline-time.monotonic()) if running else None
                try:
                    command = self._commands.get(timeout=timeout)
                except Empty:
                    command = None
                try:
                    if command:
                        generation, kind, value, requested_profile = command
                        if kind == "close":
                            break
                        with self._lock:
                            if generation != self._generation:
                                continue
                        if not connected:
                            self._capabilities = self.adapter.connect()
                            connected = True
                            if not isinstance(self._capabilities, Capabilities):
                                raise TypeError("Adapter mist expliciete mogelijkheden.")
                        if requested_profile is None:
                            raise RuntimeError("Selecteer eerst een acquisitieprofiel.")
                        if kind == "configure" or requested_profile != configured_profile:
                            self.adapter.configure(requested_profile)
                            configured_profile = requested_profile
                        if kind == "configure":
                            _, running = value
                        elif kind == "pause":
                            running = False
                        elif kind == "resume":
                            running = True
                        elif kind == "single":
                            running = False
                            self._publish(generation)
                        self._set_state("running" if running else "stopped",generation=generation)
                        deadline = time.monotonic()
                    elif running:
                        self._publish(generation)
                        # Pacing affects presentation only; the adapter owns sample timing.
                        deadline = time.monotonic()+self.interval
                except Exception as error:
                    running = False
                    message = str(error)
                    try:
                        if connected:
                            self.adapter.disconnect()
                    except Exception as cleanup_error:
                        message += "; afsluiten: "+str(cleanup_error)
                    connected = False
                    configured_profile = None
                    self._capabilities = None
                    self._set_state("error", message, generation)

        finally:
            try:
                self.adapter.disconnect()
            except Exception as error:
                self._set_state("error", str(error))
            else:
                self._set_state("disconnected")
