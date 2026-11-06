# Native oscilloscoopapp 0.3.0

Python: installeer requirements-native.txt en start python app.py.
Windows: pak de volledige native ZIP uit en start Owon_NG-0.3.0.exe. Behoud de map _internal met Python en vervangbare Qt-bibliotheken. Geen Python-installatie vereist voor de Windows-distributie.

Native Qt Widgets-interface met QPainter-golfvormcanvas. Geen browser, WebView of HTTP-server.
Werkend: gesimuleerde CKP/lambda/injector/CAN/PWM/sinus, twee kanalen, schalen/offsets, tijdzoom/pan, muis- en toetsenbordcursors, start/pauze/single, hulp, begeleide instructies, notities, JSON bewaren/openen en demo-rapportweergave.
Hardware-aansturing, triggers, decoders, diagnose en gevalideerde referentiedata zijn nog niet geïmplementeerd.
Android: de WebView-APK is ingetrokken als ontwikkelrichting. Native Android is nog niet geïmplementeerd.

Bouwen: python scripts/package.py python. Windows: installeer ook pyinstaller==6.14.2 en voer python scripts/package.py windows uit. GitHub Actions doet dit onder Native app packages.
Qt/PySide6 6.9.3 onder LGPLv3; gedeelde libraries blijven vervangbaar en licentieteksten worden meegeleverd. Bron: https://code.qt.io/pyside/pyside-setup.git/ (tag v6.9.3). Rechten en verplichtingen: https://www.qt.io/licensing/open-source-lgpl-obligations.
