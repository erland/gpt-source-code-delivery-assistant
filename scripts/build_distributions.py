#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, shutil, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = [
    "agent-progress-template.md",
    "agent-review-checklist-template.md",
    "agents-md-template.md",
    "light-delivery-workflow-template.md",
    "reference-readme-template.md",
]
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")

def version_from_args(value: str | None) -> str:
    version = value or (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not SEMVER.fullmatch(version):
        raise SystemExit(f"Ogiltig version: {version}")
    return version

def write_zip(src: Path, out: Path) -> None:
    fixed = (2020, 1, 1, 0, 0, 0)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for p in sorted(x for x in src.rglob("*") if x.is_file()):
            rel = p.relative_to(src).as_posix()
            info = zipfile.ZipInfo(rel, fixed)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, p.read_bytes())

def manifest_for(root: Path, version: str) -> dict:
    files = []
    for p in sorted(x for x in root.rglob("*") if x.is_file() and x.name != "MANIFEST.json"):
        rel = p.relative_to(root).as_posix()
        data = p.read_bytes()
        files.append({"path": rel, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    return {"package": "source-code-delivery-assistant", "format": "portable-chat-assistant", "version": version, "entrypoint": "START-HERE.md", "instructions": "assistant/instructions.md", "knowledge": [f"knowledge/{n}" for n in KNOWLEDGE], "files": files}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--version")
    ap.add_argument("--output-dir", default="dist")
    args = ap.parse_args()
    version = version_from_args(args.version)
    outdir = ROOT / args.output_dir
    work = ROOT / ".build-distributions"
    shutil.rmtree(work, ignore_errors=True); shutil.rmtree(outdir, ignore_errors=True)
    outdir.mkdir(parents=True); work.mkdir()

    custom = work / "custom"
    custom.mkdir()
    shutil.copy2(ROOT / "gpt-instructions.md", custom / "gpt-instructions.md")
    shutil.copy2(ROOT / "conversation-starters.md", custom / "conversation-starters.md")
    shutil.copy2(ROOT / "README.md", custom / "README.md")
    (custom / "VERSION").write_text(version + "\n", encoding="utf-8")
    shutil.copytree(ROOT / "knowledge", custom / "knowledge")

    portable = work / "portable"
    (portable / "assistant").mkdir(parents=True)
    (portable / "knowledge").mkdir()
    shutil.copy2(ROOT / "portable/START-HERE.md", portable / "START-HERE.md")
    shutil.copy2(ROOT / "gpt-instructions.md", portable / "assistant/instructions.md")
    shutil.copy2(ROOT / "conversation-starters.md", portable / "assistant/conversation-starters.md")
    for name in KNOWLEDGE:
        shutil.copy2(ROOT / "knowledge" / name, portable / "knowledge" / name)
    (portable / "VERSION").write_text(version + "\n", encoding="utf-8")
    (portable / "MANIFEST.json").write_text(json.dumps(manifest_for(portable, version), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    write_zip(custom, outdir / f"source-code-delivery-assistant-custom-gpt-v{version}.zip")
    write_zip(portable, outdir / f"source-code-delivery-assistant-chat-v{version}.zip")
    shutil.rmtree(work)
    print(f"Built distributions for {version}")
    return 0
if __name__ == "__main__": raise SystemExit(main())
