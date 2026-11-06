"""Schema 2 JSON recording; atomic replacement, integrity digest and v1 migration."""
from dataclasses import asdict, replace
import hashlib
import hmac
import json
import os
from pathlib import Path
import tempfile
from native.capture import Capture, ChannelConfig, ViewState

MAX_BYTES = 64 * 1024 * 1024

def encoded(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("utf8")

def note_checked(note):
    if not isinstance(note, str) or len(note) > 20000:
        raise ValueError("Notitie moet tekst van maximaal 20000 tekens zijn.")
    return note

def save_recording(path, capture, note="", view=None):
    body = {"schema": 2, "capture": asdict(capture), "note": note_checked(note), "view": asdict(view or ViewState())}
    digest = hashlib.sha256(encoded(body)).hexdigest()
    data = encoded(dict(body, sha256=digest))
    if len(data) > MAX_BYTES:
        raise ValueError("Opname is te groot.")
    path = Path(path)
    # Write/fsync before replacement: a failed save must preserve the old recording.
    descriptor, temporary = tempfile.mkstemp(prefix="."+path.name+".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as file:
            file.write(data)
            file.flush()
            os.fsync(file.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Dubbele JSON-sleutel.")
        result[key] = value
    return result

def load_recording(path):
    with Path(path).open("rb") as file:
        data = file.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("Opname is te groot.")
    try:
        doc = json.loads(data, object_pairs_hook=unique_object)
        if not isinstance(doc, dict) or type(doc.get("schema")) is not int:
            raise ValueError("Geen opnameobject.")
        if doc["schema"] == 1:
            if doc.get("source") not in ("simulation", "import") or doc.get("original", "simulation") != "simulation":
                raise ValueError("Ongeldige oude demoherkomst.")
            frame = Capture(doc["profile"], doc["rate"], doc["channels"], "import", "simulation", device_id="legacy-demo", received_at_ns=None)
            return frame, note_checked(doc.get("note", "")), ViewState()
        if doc["schema"] != 2 or set(doc) != {"schema", "capture", "view", "note", "sha256"}:
            raise ValueError("Niet-ondersteund opnameformaat.")
        digest = doc.pop("sha256")
        if not isinstance(digest, str) or not hmac.compare_digest(digest, hashlib.sha256(encoded(doc)).hexdigest()):
            raise ValueError("Integriteitscontrole mislukt: opname is beschadigd of gewijzigd.")
        values = doc["capture"]
        configs = tuple(ChannelConfig(**c) for c in values["channel_config"])
        frame = Capture(**dict(values, channel_config=configs))
        return replace(frame, source="import"), note_checked(doc["note"]), ViewState(**doc["view"])
    except (KeyError, TypeError, OverflowError, UnicodeError) as error:
        raise ValueError("Ongeldige opname-inhoud.") from error
