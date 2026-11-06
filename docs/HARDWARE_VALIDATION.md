# OWON VDS1022I — open hardware work

No physical scope was available for this development. The adapter boundary deliberately rejects connection/configuration/acquisition. No supported ranges, sample-rate limits, USB endpoints, ADC conversion, trigger semantics or calibration values are invented.

| Required check | Status | Evidence needed |
|---|---|---|
| USB identity and Windows/Linux driver/permissions | OPEN | Read-only enumeration of the actual instrument, OS/driver versions |
| Firmware provenance and redistribution rights | OPEN | Authorized source, required versions and explicit redistribution permission |
| Initialization, endpoints, transfer framing and timeouts | OPEN | Device captures and disconnect/reconnect tests |
| Applied settings vs requested settings | OPEN | Measured ranges/sample rates/record lengths; explicit rejection of unsupported combinations |
| Raw ADC representation to volts | OPEN | Known stable input, channel/probe/calibration metadata, clipping and offset checks |
| Sample clock, frame boundaries and lost-data detection | OPEN | Known-frequency signal, long acquisition, dropped-transfer recovery |
| Trigger conditions/level/position | OPEN | Known edge/pulse stimulus and actual trigger position in raw capture |
| Channel mapping and common ground | OPEN | Confirm physical mapping; both grounds remain on the same potential |
| Stop, timeout, unplug and reconnect | OPEN | Bounded cancellation and actionable errors under actual USB failures |
| Hardware decoder accuracy | OPEN | Known bus captures at multiple levels/rates/noise conditions |
| Probe safety and vehicle-specific procedures | OPEN | Rated accessories and approved procedures; no high-energy connection authorization from demo profiles |

The current simulator validates application contracts, worker lifecycle and capture persistence. It does not establish hardware correctness. A connection error is presented rather than silently substituting simulated data. Source labels must remain DEMO or IMPORTED until genuinely validated live hardware is connected.

Native Android, continuous lossless streaming recording, raw ADC packet preservation and a driver implementation are separate outstanding work. Current schema stores the supplied voltage samples exactly; it does not claim to preserve raw USB/ADC data that has never been acquired.
