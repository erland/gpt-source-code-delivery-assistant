#!/usr/bin/env python3
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
EVAL_DIR=ROOT/"evals"/"instruction-adherence"
REQUIRED_IDS={
    "precedence-001",
    "mode-routing-001",
    "one-step-only-001",
    "plan-progress-conflict-001",
    "zip-root-shape-001",
    "verification-honesty-001",
    "package-before-complete-001",
    "install-repair-source-scope-001",
}

def parse_top_level_scalar(text: str, key: str):
    m=re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", text)
    if not m:
        return None
    value=m.group(1).strip()
    if len(value)>=2 and value[0]==value[-1] and value[0] in {"'", '"'}:
        value=value[1:-1]
    return value

def has_nonempty_list(text: str, key: str):
    # Controlled eval YAML emitted by yaml.safe_dump uses:
    #   key:
    #   - item
    return re.search(rf"(?ms)^\s{{2}}{re.escape(key)}:\s*\n(?:\s{{2}}- .+(?:\n\s{{4,}}.+)*\n?)+", text) is not None

def main():
    errors=[]
    ids=set()
    files=sorted(EVAL_DIR.glob("*.yaml"))
    for p in files:
        text=p.read_text(encoding="utf-8")
        for k in ["id","title","criticality","input"]:
            if parse_top_level_scalar(text,k) is None:
                errors.append(f"{p.name}: missing {k}")
        if re.search(r"(?m)^expected:\s*$", text) is None:
            errors.append(f"{p.name}: missing expected")
        if not has_nonempty_list(text,"required"):
            errors.append(f"{p.name}: expected.required empty")
        if not has_nonempty_list(text,"forbidden"):
            errors.append(f"{p.name}: expected.forbidden empty")
        doc_id=parse_top_level_scalar(text,"id")
        if doc_id:
            ids.add(doc_id)

    missing=REQUIRED_IDS-ids
    if missing:
        errors.append(f"Missing required eval IDs: {sorted(missing)}")

    instr=(ROOT/"gpt-instructions.md").read_text(encoding="utf-8")
    boot=(ROOT/"portable"/"START-HERE.md").read_text(encoding="utf-8")

    if len(instr)>8000:
        errors.append(f"Instruction exceeds 8000 chars: {len(instr)}")

    instr_markers=[
        "## Precedence",
        "## Mode routing",
        "### Knowledge routing",
        "1. **READ**",
        "2. **SELECT**",
        "3. **LOCK**",
        "4. **IMPLEMENT**",
        "5. **VERIFY**",
        "6. **PROGRESS**",
        "7. **PACKAGE**",
        "8. **STOP**",
        "`selected_step`",
        "Exactly one delivery-plan step may be completed per response",
        "If plan and progress are materially inconsistent",
        "ZIP root shape",
        "An EXECUTE response is not complete until the updated zip has actually been created",
        "Never claim verification passed unless it actually ran and passed",
        "Do not modify application source code unless the user explicitly requests it",
    ]
    for marker in instr_markers:
        if marker not in instr:
            errors.append(f"Instruction missing marker: {marker}")

    boot_markers=[
        "READ → SELECT → LOCK → IMPLEMENT → VERIFY → PROGRESS → PACKAGE → STOP",
        "`selected_step`",
        "root-shape",
        "uppdaterad ZIP faktiskt skapats",
        "INSTALL/REPAIR ändrar inte applikationskod",
    ]
    for marker in boot_markers:
        if marker not in boot:
            errors.append(f"Bootstrap missing marker: {marker}")

    if errors:
        print("FAILED")
        for e in errors:
            print("-",e)
        return 1

    print(f"Instruction-adherence contract OK: {len(files)} eval cases")
    print(f"Instruction chars: {len(instr)}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
