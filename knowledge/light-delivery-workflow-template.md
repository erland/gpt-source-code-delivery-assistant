# Lightweight Delivery Workflow Template

Use this workflow when adding repository-owned delivery instructions to a source-code zip.

## Required files

- `AGENTS.md`
- `docs/delivery-plan.md`
- `docs/agent-progress.md`
- `docs/agent-review-checklist.md`
- `docs/reference/README.md`

## Purpose

The workflow makes a source-code zip self-contained so a user can ask:

```text
Follow AGENTS.md and implement next step.
```

The repository's `AGENTS.md` is authoritative for execution.

The GPT may install or repair these files, but execution should always follow the repository-owned instructions first.

## Design principle

The GPT is a convenience wrapper.

The repository owns:

- execution rules in `AGENTS.md`
- active work in `docs/delivery-plan.md`
- progress in `docs/agent-progress.md`
- quality checks in `docs/agent-review-checklist.md`
- project-specific reference material in `docs/reference/`
