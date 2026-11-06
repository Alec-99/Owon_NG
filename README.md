# Owon NG — native oscilloscoopapp

Versie 0.3.0 is een native Python/Qt-app met een QPainter-golfvormcanvas. De oude browserlaunchers en WebView-verpakking zijn verwijderd. De HTML/TypeScript-prototypes blijven uitsluitend als ontwerpreferentie aanwezig.

Start:

    python -m pip install -r requirements-native.txt
    python app.py

De workflow **Native app packages** bouwt op Windows een ZIP met Owon_NG-0.3.0.exe en de vereiste Qt/Python-bibliotheken. Pak de hele ZIP uit. De Python-brondistributie heet Owon_NG-0.3.0-python-native.zip.

Werkend: twee kanalen met zichtbaarheid, V/div en offset; tijdbasis en verschuiven; sleepbare en met toetsenbord bedienbare cursors met Δt/ΔV; start/pauze/single; Vpp/RMS van synthetische samples; CKP/lambda/injector/CAN/PWM/sinus-fixtures; hulp met technische details; begeleide instructies; notities; native bestandsdialogen met JSON bewaren/openen; bibliotheek, opnamegeschiedenis en demo-rapportweergave.

Alle signalen zijn expliciet DEMO of geïmporteerde demo-opnames. USB-aansturing, echte triggers, protocoldecoders, gevalideerde referentiegolfvormen en diagnostische algoritmen zijn nog niet geïmplementeerd. De rapportweergave is nog geen rapportexport. Een native Android-app is nog niet gebouwd; de oude WebView-APK is niet de gewenste app.

Veiligheid: de VDS1022I-ingangskanalen delen een gemeenschappelijke massa. Sluit aardklemmen nooit op verschillende potentialen aan. Live hoogspanning vereist passende probes en een gevalideerde procedure.

Zie docs/NATIVE_APP.md voor bouwen/licenties en docs/UI_SPEC.md voor de oorspronkelijke producteisen.

Controle:

    python -m unittest discover -s tests -p test_native.py -v

Qt/PySide6 wordt onder LGPLv3 gebruikt. De projectlicentie is nog niet gekozen. Zie docs/THIRD_PARTY.md.
