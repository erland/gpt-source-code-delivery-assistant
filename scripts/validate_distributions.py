#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
KNOWLEDGE=sorted(p.name for p in (ROOT/'knowledge').glob('*.md'))

def instruction_text(): return (ROOT/'gpt-instructions.md').read_text(encoding='utf-8')

def data(z, n): return z.read(n)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--version'); ap.add_argument('--output-dir', default='dist'); a=ap.parse_args()
    v=a.version or (ROOT/'VERSION').read_text().strip(); d=ROOT/a.output_dir
    cp=d/f'source-code-delivery-assistant-custom-gpt-v{v}.zip'; pp=d/f'source-code-delivery-assistant-chat-v{v}.zip'
    for p in (cp,pp):
        if not p.exists(): raise SystemExit(f'Saknas: {p}')
        with zipfile.ZipFile(p) as z: bad=z.testzip()
        if bad: raise SystemExit(f'Korrupt ZIP {p}: {bad}')
    instr=instruction_text()
    if len(instr)>8000: raise SystemExit(f'Instruktionen är för lång: {len(instr)}')
    for marker in [
        '## Precedence','## Mode routing','**INSTALL**','**EXECUTE**','**REPAIR**','### Knowledge routing',
        'Do not load or apply generic workflow templates',
        '1. **READ**','2. **SELECT**','3. **LOCK**','4. **IMPLEMENT**','5. **VERIFY**','6. **PROGRESS**','7. **PACKAGE**','8. **STOP**',
        '`selected_step`','Exactly one delivery-plan step may be completed per response',
        'If plan and progress are materially inconsistent',
        'An EXECUTE response is not complete until the updated zip has actually been created',
        '## Mode invariants','ZIP root shape'
    ]:
        if marker not in instr: raise SystemExit(f'Instruktionen saknar runtime-markör: {marker}')
    with zipfile.ZipFile(cp) as z:
        assert data(z,'gpt-instructions.md')==(ROOT/'gpt-instructions.md').read_bytes()
        assert data(z,'conversation-starters.md')==(ROOT/'conversation-starters.md').read_bytes()
        assert data(z,'VERSION').decode().strip()==v
        if any(n.startswith('examples/') for n in z.namelist()): raise SystemExit('Custom GPT innehåller examples/')
        for n in KNOWLEDGE: assert data(z,f'knowledge/{n}')==(ROOT/'knowledge'/n).read_bytes()
    with zipfile.ZipFile(pp) as z:
        assert data(z,'assistant/instructions.md')==(ROOT/'gpt-instructions.md').read_bytes()
        assert data(z,'assistant/conversation-starters.md')==(ROOT/'conversation-starters.md').read_bytes()
        assert data(z,'VERSION').decode().strip()==v
        if any(n.startswith('examples/') for n in z.namelist()): raise SystemExit('Portable innehåller examples/')
        for n in KNOWLEDGE: assert data(z,f'knowledge/{n}')==(ROOT/'knowledge'/n).read_bytes()
        start=data(z,'START-HERE.md').decode('utf-8')
        for marker in [
            'Mode routing','INSTALL','EXECUTE','REPAIR','repositoryts eget `AGENTS.md`','generiska templates','`examples/`',
            'EXECUTE state machine','READ → SELECT → LOCK → IMPLEMENT → VERIFY → PROGRESS → PACKAGE → STOP',
            '`selected_step`','root-shape','uppdaterad ZIP faktiskt skapats'
        ]:
            if marker not in start: raise SystemExit(f'START-HERE saknar markör: {marker}')
        m=json.loads(data(z,'MANIFEST.json')); assert m['version']==v
        for f in m['files']:
            assert hashlib.sha256(data(z,f['path'])).hexdigest()==f['sha256']
    print(f'Validation OK for {v}')
if __name__=='__main__': main()
