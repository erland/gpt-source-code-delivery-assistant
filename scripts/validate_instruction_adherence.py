#!/usr/bin/env python3
from pathlib import Path
import yaml

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

def main():
    errors=[]
    docs=[]
    for p in sorted(EVAL_DIR.glob("*.yaml")):
        d=yaml.safe_load(p.read_text(encoding="utf-8"))
        docs.append(d)
        for k in ["id","title","criticality","input","expected"]:
            if k not in d: errors.append(f"{p.name}: missing {k}")
        exp=d.get("expected",{})
        if not exp.get("required"): errors.append(f"{p.name}: expected.required empty")
        if not exp.get("forbidden"): errors.append(f"{p.name}: expected.forbidden empty")

    ids={d.get("id") for d in docs}
    missing=REQUIRED_IDS-ids
    if missing: errors.append(f"Missing required eval IDs: {sorted(missing)}")

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
        for e in errors: print("-",e)
        return 1
    print(f"Instruction-adherence contract OK: {len(docs)} eval cases")
    print(f"Instruction chars: {len(instr)}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
