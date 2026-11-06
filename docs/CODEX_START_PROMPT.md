# Startprompt voor Codex — Owon NG UI-001

Je bent de implementerende Codex-agent voor **https://github.com/Alec-99/Owon_NG**.

Ons doel is software met de **kwaliteit, betrouwbaarheid en intuïtieve gebruikerservaring van PicoScope**, specifiek voor zowel automotive diagnostiek als elektronica. Kopieer niet het uiterlijk of propriëtaire elementen van PicoScope. Het project moet begeleide componenttests, referentiegolfvormen, contextuele uitleg via (i)-knoppen, echte oscilloscoopbediening en degelijke opname-/analyseflows ondersteunen. De **OWON VDS1022I** is de eerste beoogde hardware.

**Ontwikkelvolgorde is verplicht: eerst de volledige UI/UX, pas daarna de echte features, hardware-USB-driver, decoders en automatische diagnose.** Werk nu uitsluitend aan **UI-001**: een hoogwaardige, modulaire frontend met coherente simulatieflows. Deze eerste batch is de basis voor de rest van de UI-fase. Stop na de PR, zodat ik kan beoordelen.

## Je eerste stappen

1. Open de repository en controleer branches, open PR's, CI en bestaande bestanden. De voorbereidende documenten staan momenteel op **\`feat/first-ux-prototype\`** (draft PR #1); \`main\` bevat mogelijk nog niet alles.
2. Lees volledig: \`AGENTS.md\`, \`docs/START_HERE.md\`, \`docs/UI_SPEC.md\`, \`docs/ROADMAP.md\`, \`docs/tasks/UI-001.md\`, \`docs/ARCHITECTURE.md\`, \`docs/REFERENCE_REPOS.md\` en \`docs/THIRD_PARTY.md\`. Volg die documenten als taakafbakening.
3. Baseer je werkbranch **\`codex/UI-001-app-foundation\`** op \`feat/first-ux-prototype\` zolang PR #1 niet gemerged is. Als dat ondertussen wél gebeurd is, vertrek dan van de actuele \`main\` en pas het PR-doel aan.
4. Onderzoek relevante open-source repos en libraries voor herbruikbare concepten, UI-componenten of code (onder andere **neowon, PulseView, OpenHantek** en andere goede kandidaten). Je mag permissief gelicentieerde code hergebruiken mits exacte licentie-, copyright-, NOTICE- en dependencycontrole en registratie in \`docs/THIRD_PARTY.md\`. Kopieer geen code zonder expliciete hergebruiklicentie, geen GPL-code zonder gekozen compatibele projectlicentie, en geen propriëtaire PicoScope- of OWON-assets.
5. Bouw de modulaire UI en een werkende lokale demo volgens **UI-001**. De hoofdschermen en navigatie moeten bruikbaar zijn, de golfvormen zijn voor deze fase **duidelijk gemarkeerde simulaties**. Zorg voor automotive en elektronica, met minstens één volledige gesimuleerde componenttest (bv. CKP) en één elektronica-test (bv. PWM). Voeg duidelijke uitlegknoppen en veiligheidsinstructies toe. De OWON-kanalen hebben een gemeenschappelijke massa.
6. Voeg tests, een automatische CI-check, documentatie en runcommando's toe. Behoud het bestaande standalone prototype als referentie. Gebruik geen echte USB- of hoogspanningshardwaretests.
7. Maak één goed beschreven pull request met screenshots/visuals indien mogelijk, testresultaten, licentiebewijs, beperkingen en duidelijke vervolgbatches. **Merge niets. Stop na UI-001 en wacht op mijn feedback.**

Werk zelfstandig binnen dit kader, maak verstandige ontwerpkeuzes en documenteer belangrijke beslissingen. De repo-naam **Owon_NG** kan later nog veranderen.
