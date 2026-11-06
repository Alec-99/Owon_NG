# Native oscilloscoopapp 0.3.1

Python: installeer requirements-native.txt en start python app.py.
Windows: pak de volledige native ZIP uit en start Owon_NG-0.3.1.exe. Behoud de map _internal met Python en vervangbare Qt-bibliotheken. Geen Python-installatie vereist voor de Windows-distributie.

Native Qt Widgets-interface met QPainter-golfvormcanvas. Geen browser, WebView of HTTP-server.
Werkend: gesimuleerde CKP/lambda/injector/CAN/PWM/sinus, twee kanalen, schalen/offsets, tijdzoom/pan, muis- en toetsenbordcursors, start/pauze/single, hulp, begeleide instructies, notities, JSON bewaren/openen en demo-rapportweergave.
Hardware-aansturing, triggers, extra decoders, diagnose en gevalideerde referentiedata zijn nog niet geïmplementeerd.
Android: de WebView-APK is ingetrokken als ontwikkelrichting. Native Android is nog niet geïmplementeerd.

Bouwen: python scripts/package.py python. Windows: installeer ook pyinstaller==6.14.2 en voer python scripts/package.py windows uit. GitHub Actions doet dit onder Native app packages.
Qt/PySide6 6.9.3 onder LGPLv3; gedeelde libraries blijven vervangbaar en licentieteksten worden meegeleverd. Bron: https://code.qt.io/pyside/pyside-setup.git/ (tag v6.9.3). Rechten en verplichtingen: https://www.qt.io/licensing/open-source-lgpl-obligations.

## 0.3.1 — signaalanalyse en automotive

Automotive bevat een passief PWM-solenoïdeprofiel; de app stuurt geen actuator aan.
Elektronica bevat UART 8N1 (fixture 9600 baud, bytes 55/A5), I²C (CH1 SCL, CH2 SDA; fixture A0/55 met ACK) en PWM.
Analyse werkt op samples met een vaste 2,5 V-drempel. UART vereist minimaal 8 samples per bit en meldt framingfouten. PWM rapporteert mediane periode/duty over volledige perioden. I²C toont START en bytes/ACK; nog geen volledige protocolinterpretatie. Geen ruis-/hardwarevalidatie, autobaud, herstelgarantie of diagnose. SPI en CAN-protocol zijn zichtbaar als gepland.

## 0.3.2 — instrumentindeling

Compacte native menubalk en werkbalk, kanaalinstellingen rechts, testhulp in een eigen tab en decoders/notities onder de grafiek. Het scopecanvas toont voltage- en tijdassen, fijn raster en kleurvaste CH1/CH2-labels. De bibliotheek is een tabel. Cursorbediening houdt rekening met de nieuwe grafiekmarges. Beeldcontrole uitgevoerd op 1440×960 en 1040×760.

## 0.4.0 / 0.4.1 — meetkern en decoderbanen

Opnames bewaren timing, onveranderlijke samples, kanaalmetadata en de weergave-instellingen. De simulator draait in een aparte worker met zichtbare buffer-overloop; oude frames kunnen een geïmporteerde opname niet overschrijven. Dit is nog geen continue verliesvrije recorder. Zie ACQUISITION_CORE.md en HARDWARE_VALIDATION.md.

Decodeblokken staan onder de trace op dezelfde tijdas. Analyse pauzeert de simulatie. Hex/decimaal/ASCII/binair zijn weergavekeuzes; klik een blok voor samples en tijdbereik. UART toont bytes en framing/onvolledigheidsmeldingen; I²C toont 7-bit adres/richting, data en ACK/NACK; PWM toont perioden/duty. Eén decoderbaan tegelijk. Nieuwe samples of instellingen maken oude resultaten ongeldig.
