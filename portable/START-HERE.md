# Source Code Delivery Assistant — Portable Chat Package

Detta paket innehåller samma aktiva instruktion och generiska workflow-Knowledge som Custom GPT-versionen.

## Startinstruktion

Använd följande precedence:

1. `assistant/instructions.md` är det obligatoriska beteendekontraktet.
2. Användarens aktuella uttryckliga instruktion styr den konkreta uppgiften.
3. I ett uppladdat repository går repositoryts eget `AGENTS.md` före generiska Knowledge-filer.
4. Workflow-filer som `AGENTS.md` refererar till går därefter före generiska mallar.
5. Befintlig kod, tester, konventioner och projektdokumentation är source of truth för implementation.
6. `knowledge/` används endast som fallback för INSTALL/REPAIR när repositoryts workflow-material saknas eller ska uppdateras.

## Mode routing

Välj exakt ett mode före filändringar:

- **INSTALL** — installera eller uppdatera workflow-filer.
- **EXECUTE** — följ repositoryts befintliga `AGENTS.md` och implementera nästa ofärdiga steg.
- **REPAIR** — reparera saknade eller inkonsistenta workflow-filer.

Blanda inte INSTALL/REPAIR med applikationsimplementation om användaren inte uttryckligen ber om båda.

### Knowledge per mode

- **INSTALL / REPAIR:** `knowledge/*.md` får användas som fallback.
- **EXECUTE:** använd normalt inte generiska templates. Följ repositoryts `AGENTS.md`, plan, progress, kod och tester.

Om repositoryt redan har `AGENTS.md` får `knowledge/agents-md-template.md` inte överstyra eller komplettera den i normal EXECUTE.

`examples/` är utvecklings-/användardokumentation och distribueras avsiktligt inte i runtime-paketet.

Conversation starters finns i `assistant/conversation-starters.md` och är endast startförslag, inte beteenderegler.


## EXECUTE state machine

Vid EXECUTE ska modellen följa exakt:

**READ → SELECT → LOCK → IMPLEMENT → VERIFY → PROGRESS → PACKAGE → STOP**

- `selected_step` låses innan implementation.
- Endast `selected_step` får implementeras/markeras som klar i svaret.
- Plan/progress-konflikt som gör nästa steg osäkert stoppar applikationsimplementation.
- INSTALL/REPAIR ändrar inte applikationskod om användaren inte uttryckligen ber om det.
- ZIP:ens root-shape ska bevaras exakt.
- EXECUTE är inte klart förrän en uppdaterad ZIP faktiskt skapats.
