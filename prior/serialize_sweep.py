import json,hashlib,re,html,os
import demo_oracle as D

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from guard import install as _guard_install
_guard_install(__file__)
PRIZE="14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
P=[(pid,t) for pid,t in json.load(open('wp_paras.json'))]; N=len(P)
txt=[t for _,t in P]; pid=[p for p,_ in P]
def H(b): return hashlib.md5(b if isinstance(b,bytes) else b.encode()).digest()
cands={}
# 1. raw scraped artifacts, byte for byte
for f in ('second.txt','chapter_single.txt','chapter_lf.txt','chapter_crlf.txt'):
    if os.path.exists(f): cands['raw:'+f]=open(f,'rb').read()
# 2. tagged forms
cands['tags_pid_nl']='\n'.join(f'<p data-p-id="{p}">{t}</p>' for p,t in P)
cands['tags_pid_concat']=''.join(f'<p data-p-id="{p}">{t}</p>' for p,t in P)
cands['tags_nopid']='\n'.join(f'<p>{t}</p>' for t in txt)
cands['tags_nopid_concat']=''.join(f'<p>{t}</p>' for t in txt)
cands['tags_br']='<br><br>'.join(txt)
cands['tags_br_nopid']='<br/><br/>'.join(txt)
# 3. ids with text
cands['pid_tab_text']='\n'.join(f'{p}\t{t}' for p,t in P)
cands['pid_space_text']='\n'.join(f'{p} {t}' for p,t in P)
cands['pidnl_nl']='\n'.join(f'{p}\n{t}' for p,t in P)
cands['text_only_join_nl']='\n'.join(txt)
# 4. html-escaped text
cands['escaped_nl']='\n'.join(html.escape(t,quote=True) for t in txt)
cands['escaped_tags']='\n'.join(f'<p>{html.escape(t,quote=True)}</p>' for t in txt)
# 5. typographic quotes
def typ(s):
    out=[];open_q=True
    for ch in s:
        if ch=='"':
            out.append('\u201c' if open_q else '\u201d'); open_q=not open_q
        else: out.append(ch)
    return ''.join(out)
cands['typographic']='\n'.join(typ(t) for t in txt)
# 6. BOM
cands['bom_nl']='\ufeff'+'\n'.join(txt)
# 7. no heading paragraphs (drop first 3)
cands['drop_headings']='\n'.join(txt[3:])
# 8. with trailing newline
cands['nl_trailing']='\n'.join(txt)+'\n'
hits=[]; n=0
for name,b in cands.items():
    d=H(b)
    for ix in (0,1,2,3):
        w,a=D.derive(d,f"m/44'/0'/0'/0/{ix}"); n+=1
        if a==PRIZE: hits.append((name,ix,w))
    print(f'{name:22s} len={len(b) if isinstance(b,bytes) else len(b.encode()):>6} md5={d.hex()[:10]}')
print('\nderivations',n,'hits',hits)
