#!/usr/bin/env python3
"""Validate data/levels.js: every grid/bonus word is buildable from the wheel letters (with multiplicity), the crossword is consistent
(cells agree at crossings, inside r×c, no touching/adjacent parallel words, connected, words not extended by neighbours), no duplicates,
every grid word has a Russian translation, no word hits the religion/offensive stop-lists, letters are Komi Cyrillic. Exit 1 on any error."""
import json, re, sys, os, collections
sys.path.insert(0, os.path.dirname(__file__))
from religion_filter import religious, offensive
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(f'{ROOT}/data/levels.js', encoding='utf-8').read()
D = json.loads(s[s.index('=') + 1:].rstrip().rstrip(';'))
KOMI = re.compile(r'^[абвгдеёжзиійклмнопрстуфхцчшщъыьэюяӧ]+$')
errs = []
def err(lv, m): errs.append(f"level {lv['id']}: {m}")
def check(lv):
    pool = collections.Counter(lv['l'])
    if not KOMI.match(lv['l']): err(lv, 'non-Komi letters ' + lv['l'])
    words = [x[0] for x in lv['w']]
    if len(set(words)) != len(words): err(lv, 'duplicate grid word')
    if len(words) < 3: err(lv, 'fewer than 3 words')
    for w in words + lv['b']:
        if any(collections.Counter(w)[k] > pool[k] for k in w): err(lv, f'"{w}" not buildable from {lv["l"]}')
        g = (lv['g'].get(w) or [''])[0]
        if religious(w, g) or offensive(w, g): err(lv, f'stop-listed word "{w}" ({g})')
    if set(words) & set(lv['b']): err(lv, 'word both in grid and bonus')
    if max(len(w) for w in words) != len(lv['l']): err(lv, 'longest word does not use all letters')
    for w in words:
        if w not in lv['g'] or not lv['g'][w][0]: err(lv, f'no translation for "{w}"')
    cell = {}; owner = collections.defaultdict(set)
    for w, r, c, d in lv['w']:
        dr, dc = (0, 1) if d == 'h' else (1, 0)
        for i, ch in enumerate(w):
            p = (r + dr * i, c + dc * i)
            if not (0 <= p[0] < lv['r'] and 0 <= p[1] < lv['c']): err(lv, f'"{w}" outside grid')
            if p in cell and cell[p] != ch: err(lv, f'conflict at {p}: {cell[p]} vs {ch} ("{w}")')
            cell[p] = ch; owner[p].add((w, d))
        before, after = (r - dr, c - dc), (r + dr * len(w), c + dc * len(w))
        if before in cell or after in cell: pass  # checked below after all placed
    for w, r, c, d in lv['w']:
        dr, dc = (0, 1) if d == 'h' else (1, 0)
        if (r - dr, c - dc) in cell or (r + dr * len(w), c + dc * len(w)) in cell: err(lv, f'"{w}" touches another word at an end')
    # every maximal run of ≥2 cells in a row/column must be exactly one placed word
    placed = {(w, r, c, d) for w, r, c, d in lv['w']}
    for d, (dr, dc) in (('h', (0, 1)), ('v', (1, 0))):
        for p in cell:
            if (p[0] - dr, p[1] - dc) in cell: continue
            run = ''; q = p
            while q in cell: run += cell[q]; q = (q[0] + dr, q[1] + dc)
            if len(run) >= 2 and (run, p[0], p[1], d) not in placed: err(lv, f'stray run "{run}" at {p} {d}')
    # connectivity
    if cell:
        start = next(iter(cell)); seen = {start}; st = [start]
        while st:
            a = st.pop()
            for n in ((a[0] + 1, a[1]), (a[0] - 1, a[1]), (a[0], a[1] + 1), (a[0], a[1] - 1)):
                if n in cell and n not in seen: seen.add(n); st.append(n)
        if len(seen) != len(cell): err(lv, 'crossword not connected')
for lv in D['levels'] + D['daily']: check(lv)
bases = [''.join(sorted(lv['l'])) for lv in D['levels']]
dup = [b for b, n in collections.Counter(bases).items() if n > 1]
if dup: errs.append('repeated letter sets: ' + ', '.join(dup))
if len(D['levels']) < 50: errs.append('fewer than 50 levels')
words = {x[0] for lv in D['levels'] for x in lv['w']}
print(f"levels {len(D['levels'])}, daily {len(D['daily'])}, chapters {len(D['chapters'])}, distinct grid words {len(words)}, "
      f"grid placements {sum(len(lv['w']) for lv in D['levels'])}, bonus {sum(len(lv['b']) for lv in D['levels'])}")
for e in errs[:50]: print('ERROR', e)
print('OK' if not errs else f'{len(errs)} errors'); sys.exit(1 if errs else 0)
