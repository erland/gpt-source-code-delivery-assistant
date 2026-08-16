# Source Code Delivery Assistant — GPT Setup Package

This package contains the instructions and knowledge files needed to create a custom GPT that can install and optionally execute a lightweight `AGENTS.md`-based delivery workflow in uploaded source-code zip files.

## Recommended GPT name

`Source Code Delivery Assistant`

## Recommended GPT description

`Adds, repairs, and executes a lightweight AGENTS.md-based delivery workflow for source-code zip files.`

## Files in this package

- `gpt-instructions.md` — paste this into the GPT Builder **Instructions** field.
- `conversation-starters.md` — suggested conversation starters for the GPT.
- `knowledge/agents-md-template.md` — default `AGENTS.md` template to install into repositories.
- `knowledge/agent-progress-template.md` — default progress tracking template.
- `knowledge/agent-review-checklist-template.md` — default review checklist template.
- `knowledge/light-delivery-workflow-template.md` — overview of the lightweight workflow.
- `knowledge/reference-readme-template.md` — default `docs/reference/README.md` template.
- `examples/example-user-prompts.md` — useful prompts for installing and executing the workflow.

## How to create the GPT

1. Open ChatGPT.
2. Open **Explore GPTs**.
3. Choose **Create**.
4. Open the **Configure** tab.
5. Set the name and description from above.
6. Copy the contents of `gpt-instructions.md` into the GPT instructions field.
7. Upload the files under `knowledge/` as GPT knowledge files.
8. Add the conversation starters from `conversation-starters.md`.
9. Enable file uploads and Code Interpreter / Advanced Data Analysis.
10. Save and test the GPT with a small source-code zip.

## Recommended capabilities

Enable:

- File uploads
- Code Interpreter / Advanced Data Analysis

Optional:

- Web browsing/search, only if you want the GPT to verify current tool behavior or dependency details.

Usually disable:

- Image generation
- Custom Actions, unless you later add repository integrations.

## Intended operating model

The GPT is a convenience layer. The repository remains the source of truth.

The GPT should help with:

- adding workflow files to a zip
- repairing missing or inconsistent workflow files
- converting a supplied plan into `docs/delivery-plan.md`
- following the repository's own `AGENTS.md` to implement the next incomplete step

The actual workflow should live in the repository so it can be manually customized per codebase.

## Portable Chat distribution and releases

Repositoryt kan bygga två distributionspaket från samma källfiler:

- `source-code-delivery-assistant-custom-gpt-vX.Y.Z.zip` för installation/arkivering av Custom GPT-konfigurationen.
- `source-code-delivery-assistant-chat-vX.Y.Z.zip` för användning genom att bifoga paketet i en vanlig ChatGPT-konversation och läsa `START-HERE.md` först.

Lokalt:

```bash
python3 scripts/build_distributions.py
python3 scripts/validate_distributions.py
```

Vanliga builds använder `VERSION`. Vid en publicerad GitHub Release används release-taggen som versionskälla. En release med taggen `v1.1.0` bygger därför automatiskt båda v1.1.0-paketen och bifogar dem som release assets.
