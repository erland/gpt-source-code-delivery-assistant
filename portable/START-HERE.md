# Source Code Delivery Assistant — Portable Chat Package

Detta paket gör samma instruktioner och knowledge-filer som används av Custom GPT-versionen tillgängliga i en vanlig ChatGPT-konversation.

## Användning

1. Läs `assistant/instructions.md` först och använd den som arbetsinstruktion för resten av konversationen.
2. Använd filerna i `knowledge/` som primärt referensmaterial för workflow-mallar och leveransstruktur.
3. Om användaren bifogar ett källkodsprojekt som ZIP är det projektet source of truth, enligt instruktionen.
4. Vid konflikt gäller användarens aktuella uttryckliga instruktioner före paketets instruktioner.

Conversation starters finns i `assistant/conversation-starters.md` som exempel på lämpliga startprompter.
