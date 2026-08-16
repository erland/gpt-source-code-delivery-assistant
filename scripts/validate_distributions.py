#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
KNOWLEDGE=sorted(p.name for p in (ROOT/'knowledge').glob('*.md'))

def data(z, n): return z.read(n)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--version'); ap.add_argument('--output-dir', default='dist'); a=ap.parse_args()
    v=a.version or (ROOT/'VERSION').read_text().strip(); d=ROOT/a.output_dir
    cp=d/f'source-code-delivery-assistant-custom-gpt-v{v}.zip'; pp=d/f'source-code-delivery-assistant-chat-v{v}.zip'
    for p in (cp,pp):
        if not p.exists(): raise SystemExit(f'Saknas: {p}')
        with zipfile.ZipFile(p) as z: bad=z.testzip()
        if bad: raise SystemExit(f'Korrupt ZIP {p}: {bad}')
    with zipfile.ZipFile(cp) as z:
        assert data(z,'gpt-instructions.md')==(ROOT/'gpt-instructions.md').read_bytes()
        assert data(z,'conversation-starters.md')==(ROOT/'conversation-starters.md').read_bytes()
        assert data(z,'VERSION').decode().strip()==v
        for n in KNOWLEDGE: assert data(z,f'knowledge/{n}')==(ROOT/'knowledge'/n).read_bytes()
    with zipfile.ZipFile(pp) as z:
        assert data(z,'assistant/instructions.md')==(ROOT/'gpt-instructions.md').read_bytes()
        assert data(z,'assistant/conversation-starters.md')==(ROOT/'conversation-starters.md').read_bytes()
        assert data(z,'VERSION').decode().strip()==v
        for n in KNOWLEDGE: assert data(z,f'knowledge/{n}')==(ROOT/'knowledge'/n).read_bytes()
        m=json.loads(data(z,'MANIFEST.json')); assert m['version']==v
        for f in m['files']:
            assert hashlib.sha256(data(z,f['path'])).hexdigest()==f['sha256']
    print(f'Validation OK for {v}')
if __name__=='__main__': main()
