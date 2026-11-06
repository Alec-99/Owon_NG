# Acquisition and recording core — 0.4.0

## Native boundaries

- capture.py: frozen captures and channel metadata; defensively copied tuples of voltage samples. Rate, stream ID, first sample index and frame index describe sample timing independently of repaint scheduling. Host receive time is an integer Unix nanosecond timestamp, not a device timestamp.
- acquisition.py: ScopeAdapter protocol, deterministic indexed simulator and one adapter-owner worker. Start/pause/single/configure operate through commands. Generation tokens discard late frames from superseded requests; profile changes create a new stream. read_frame has an explicit bounded timeout contract. The future hardware adapter must honor it.
- A bounded preview queue reports overflow separately from frames skipped by coalescing for display. It is NOT a lossless continuous recorder. Closing the window joins the worker; an unresponsive adapter prevents a falsely successful close.
- rendering.py: min/max envelopes preserve sampled extrema when several samples map to one pixel. This is a display representation, not filtering, interpolation or additional physical bandwidth.

## Schema 2 recordings

UTF-8 JSON includes immutable capture metadata, two channels, channel units/probe/coupling/calibration metadata, notes and separate display state (time/div, pan, V/div, offsets, channel visibility, cursors and decoder selection). All current voltage sample values round-trip without quantization; raw USB/ADC counts are not present. Unknown physical probe/coupling/calibration values remain unknown/unvalidated.

SHA-256 covers the canonical body including sample data and settings. This detects accidental modification/corruption, NOT malicious re-signing or authenticity. Schema/type/size checks reject invalid files. Saving fsyncs a temporary file and atomically replaces the destination; failure before replacement preserves the previous recording. No guarantee is made about power-loss durability on arbitrary filesystems.

Import preserves original provenance and IDs and marks the presentation IMPORTED. An imported hardware claim is never treated as a verified live connection. Schema 1 demo files migrate with unknown original receive time and default view settings; missing old metadata is not invented. This release can open known application profiles; arbitrary external instrument formats are not implemented.

## Validation

python -m unittest discover -s tests -p test_core.py -v
QT_QPA_PLATFORM=offscreen python -m unittest discover -s tests -p test_native.py -v

Tests exercise binary-float round-trip (including negative zero), capture immutability, atomic-write failure, corrupt/invalid/legacy files, view restoration, in-flight profile changes, buffer overflow, error recovery, single/pause and shutdown, plus spike-preserving rendering. Windows CI runs both suites before creating the native packages.

See HARDWARE_VALIDATION.md for work that needs a physical instrument. No USB commands or proprietary firmware are shipped.
