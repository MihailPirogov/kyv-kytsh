#!/usr/bin/env python3
"""Word-form frequencies from the kv.wikipedia dump (src/kvwiki.xml.bz2) -> src/kvwiki_freq.json (forms with count>=2)."""
import bz2, re, collections, json, os
S = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')
# Komi texts often use Latin i / ö or other look-alikes instead of Cyrillic і / ӧ
TR = str.maketrans({'i': 'і', 'I': 'І', 'ö': 'ӧ', 'Ö': 'Ӧ', 'ё': 'ё'})
TOK = re.compile(r'[а-яёіӧ]+')
c = collections.Counter(); intext = False
with bz2.open(f'{S}/kvwiki.xml.bz2', 'rt', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if '<text' in line: intext = True
        if intext: c.update(TOK.findall(line.translate(TR).lower()))
        if '</text>' in line: intext = False
json.dump({w: n for w, n in c.items() if n >= 2}, open(f'{S}/kvwiki_freq.json', 'w'), ensure_ascii=False)
print('forms', len(c), 'kept', sum(1 for n in c.values() if n >= 2))
