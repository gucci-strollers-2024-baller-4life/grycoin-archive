import json,hashlib,sys,itertools,time
sys.path.insert(0,'harness')
import btc

# AUDIT GUARD 2026-10-31: certified-corpus parity + drift-pattern refusal. See guard.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from guard import install as _guard_install
_guard_install(__file__)
LIVE='14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'
OLD='1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC'
paras=json.load(open('chapter_paras_exact.json'))
print(len(paras))
first=[next((c for c in p if c.isalpha()),'') for p in paras]
last=[next((c for c in reversed(p) if c.isalpha()),'') for p in paras]
sets={
 'ITASM':'ITASM','SATOSHI':'SATOSHI','THOMAS':'THOMAS','NAKAMOTO':'NAKAMOTO',
 'FINNEY':'FINNEY','HALFINNEY':'HALFINNEY','STNM':'STNM','AOI':'AOI',
 'SH':'SH','OH':'OH','SATOMI':'SATOMI',
}
for n,s in sets.items():
    out=sum(1 for f in first if f.upper() not in s)
    print(n,'anomalies',out)
print('firsts',''.join(first))
