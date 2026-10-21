#!/usr/bin/env python3
"""Komi (Komi-Zyrian) lexicon + crossword layout for the Komi word game (imported by build_game.py).
Sources (in src/, see SOURCES.md):
  ru_kv.jsonl      - Komi-Zyrian entries of the Russian Wiktionary (ru.wiktionary.org), extracted by Wiktextract / kaikki.org.
                     CC BY-SA 4.0 (+GFDL). Headwords, Russian translations, examples, forms. The ONLY source of shipped glosses/cards.
  en_kv.jsonl      - Komi-Zyrian entries of the English Wiktionary (kaikki.org), CC BY-SA 4.0: extra headwords (bonus only), English fallback gloss.
  kvwiki_freq.json - word-form counts from the kv.wikipedia dump (tools/kvwiki_freq.py); only numbers are used.
"""
import json, re, random, collections, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = f'{ROOT}/src'; T = f'{ROOT}/tools'; OUT = ROOT
sys.path.insert(0, T)
from religion_filter import religious, offensive
random.seed(42)
freq = json.load(open(f'{S}/kvwiki_freq.json'))
NORM = str.maketrans({'i': 'і', 'ö': 'ӧ', 'I': 'І', 'Ö': 'Ӧ'})
ru_extra = json.load(open(f'{S}/ru_gloss_extra.json')) if os.path.exists(f'{S}/ru_gloss_extra.json') else {}
LET = re.compile(r'^[а-яёіӧ]{3,8}$')
LOAN_LET = re.compile(r'[щёфъ]')            # letters found almost only in Russian loans
POS_RU = {'noun': 'сущ.', 'verb': 'гл.', 'adj': 'прил.', 'adv': 'нареч.', 'num': 'числ.', 'pron': 'мест.'}
# special-field labels: such words are valid (bonus) but not crossword words
SPECIAL = ('хим.', 'мед.', 'физ.', 'анат.', 'лингв.', 'книжн.', 'диал.', 'матем.', 'истор.', 'техн.', 'биол.', 'астрон.', 'филол.', 'филос.',
           'биохим.', 'геол.', 'спец.', 'физиол.', 'грам.', 'экон.', 'юр.', 'минер.', 'комп.', 'устар.', 'редк.', 'прост.', 'сл.', 'полит.', 'воен.',
           'геометр.', 'информ.', 'полигр.', 'рег.', 'страд.', 'понуд.', 'деепр.', 'прич.', 'ист.', 'разг.', 'бот.', 'зоол.', 'церк.', 'перен.', 'шутл.', 'пренебр.', 'неодобр.', 'фольк.', 'этн.', 'мифол.', 'рел.')
LAB_RE = re.compile(r'^((?:[а-яёА-Я]+\.\s*)+)')
REF_RE = re.compile(r'^(?:см\.|то же,? что|словоформа|форма|мн\. ч\.|прич\. от|деепр\. от)', re.I)

def split_label(g):
    m = LAB_RE.match(g)
    if not m: return '', g.strip()
    lab = m.group(1).strip()
    if lab in ('см.',): return '', g.strip()
    return lab, g[m.end():].strip()

def clean_gloss(g):
    g = re.sub(r'\s*\(аналогично русскому слову\)', '', g)
    return re.sub(r'\s+', ' ', g).strip(' ;,')

# ---------- read the Russian Wiktionary ----------
entries = collections.defaultdict(list)    # headword -> list of entry dicts (homonyms)
form_of = {}                               # inflected form -> lemma
def form_count(j):
    return sum(freq.get(f['form'], 0) for f in j.get('forms', []) if 'romanization' not in f.get('tags', []) and ' ' not in f['form'])
for l in open(f'{S}/ru_kv.jsonl', encoding='utf-8'):
    j = json.loads(l); w = j['word'].lower().strip(); pos = j.get('pos')
    if pos not in POS_RU: continue
    w = w.translate(NORM); inf = ''
    senses = []
    for s in j.get('senses', []):
        gl = [x for x in s.get('glosses', []) if x]
        if not gl: continue
        lab, d = split_label(clean_gloss(gl[0]))
        if not d: continue
        ex = []
        for e in s.get('examples', [])[:3]:
            t = (e.get('text') or '').strip(); tr = (e.get('translation') or '').strip()
            if t and tr and len(t) < 160: ex.append([t, tr, ''])
        senses.append(dict(lab=lab, d=d, ex=ex))
    if not senses: continue
    extra = []
    for key, name in (('synonyms', 'Синонимы'), ('antonyms', 'Антонимы'), ('derived', 'Производные')):
        it = [x['word'] for x in j.get(key, []) if x.get('word') and not religious(x['word'])][:6]
        if it: extra.append(dict(kind=name, items=it))
    e = dict(pos=pos, inf=inf, senses=senses, extra=extra, f=form_count(j) + freq.get(w, 0) + (freq.get(inf, 0) if inf else 0))
    entries[w].append(e)
    for f in j.get('forms', []):
        fw = f['form'].lower()
        if 'romanization' in f.get('tags', []) or not LET.match(fw) or fw == w: continue
        form_of.setdefault(fw, w)

wk_en = {}
for l in open(f'{S}/en_kv.jsonl', encoding='utf-8'):
    j = json.loads(l)
    if j.get('pos') not in POS_RU: continue
    gl = [g for s in j.get('senses', []) for g in s.get('glosses', []) if 'letter of the' not in g]
    if gl: wk_en.setdefault(j['word'].lower().translate(NORM), gl)

# ---------- cards ----------
def all_text(es): return ' '.join(s['lab'] + ' ' + s['d'] + ' ' + ' '.join(x[1] for x in s['ex']) for e in es for s in e['senses'])
def resolve_ref(d, depth=0):
    """'см. X' -> X's first gloss"""
    m = re.match(r'^см\.\s*([а-яёіӧ]+)', d)
    if m and depth < 2 and m.group(1) in entries:
        return resolve_ref(entries[m.group(1)][0]['senses'][0]['d'], depth + 1)
    return d

UD = {}   # word -> {g: first gloss, loan, card, special, f}
BANNED = set(); NAMES = set()
for w, es in entries.items():
    if not LET.match(w): continue
    first_txt = es[0]['senses'][0]['lab'] + ' ' + es[0]['senses'][0]['d']
    if re.search(r'(?:мужское|женское) имя|^[А-ЯЁ]', es[0]['senses'][0]['d']): NAMES.add(w); continue   # personal / place names
    if religious(w, first_txt) or offensive(w, first_txt, es[0]['senses'][0]['lab']): BANNED.add(w); continue
    hom = []
    for e in es:
        ss = []
        for s in e['senses'][:6]:
            d = resolve_ref(s['d'])
            if religious('', s['lab'] + ' ' + d) or offensive('', d, s['lab']): continue      # drop the sense, keep the word
            ex = [x for x in s['ex'] if not (religious(x[0], x[1]) or offensive('', x[1]) or any(religious(t) or offensive(t) for t in re.findall(r'[а-яёіӧ]+', x[0].lower())))]
            ss.append(dict(n=len(ss) + 1, lab=s['lab'], d=d[:200], ex=ex[:2]))
        if ss: hom.append(dict(pos=e['pos'], senses=ss))
    if not hom: BANNED.add(w); continue
    first = hom[0]['senses'][0]
    g = first['d']
    loan = bool(LOAN_LET.search(w)) or w in re.findall(r'[а-яё]+', ' '.join(s['d'].lower() for h in hom for s in h['senses'][:1]))
    special = all(any(x in s['lab'] for x in SPECIAL) for h in hom for s in h['senses'][:1])
    ref_only = all(REF_RE.match(s['d']) for h in hom for s in h['senses'])
    gram = ', '.join(sorted({POS_RU[e['pos']] for e in es}))
    inf = next((e['inf'] for e in es if e['inf']), '')
    if inf: gram += ' (инф. ' + inf + ')'
    ex_by = {}
    for e in es:
        for x in e['extra']:
            lst = ex_by.setdefault(x['kind'], [])
            lst += [i for i in x['items'] if i not in lst]
    extra = [dict(kind=k, items=v[:6]) for k, v in ex_by.items()][:3]
    UD[w] = dict(g=None if ref_only else g, loan=loan, special=special or ref_only, f=sum(e['f'] for e in es),
                 card=dict(stress='', gram=gram, hill='', hom=hom, extra=extra, src='wkru'))
for w, g in ru_extra.items():   # hand-checked Russian glosses for en.wiktionary-only headwords (src/ru_gloss_extra.json)
    if w in UD or not LET.match(w) or religious(w, g) or offensive(w, g): continue
    UD[w] = dict(g=g, loan=bool(LOAN_LET.search(w)), special=False, f=freq.get(w, 0),
                 card=dict(stress='', gram='', hill='', hom=[dict(pos='', senses=[dict(n=1, lab='', d=g, ex=[])])], extra=[], src='wken'))
# ---------- GiellaLT dict-kpv-rus (CC BY 4.0): main extra source of Russian translations ----------
from gt_dict import load as gt_load
GT = gt_load(f'{S}/dict-kpv-rus') if os.path.isdir(f'{S}/dict-kpv-rus') else {}
def gt_clean(d):
    d = d.split('||')[0]; d = re.sub(r'\s*\([^)]*$', '', d)
    return re.sub(r'\s+', ' ', d).strip(' ;,.')
GT_ADDED = 0
for w, es in GT.items():
    if w in UD or w in BANNED or w in NAMES or not LET.match(w): continue
    hom = []
    for e in es:
        ss = []
        for x in e['senses'][:6]:
            if 'dialect' in x['rng']: continue
            l2, d = split_label(re.sub(r'^\d+\.\s*', '', gt_clean(x['d']))); xl = (x['lab'] + ' ' + l2).strip()
            if not d or re.match(r'^(?:послелог|частица|союз|междометие|возглас|суффикс)', d) or religious(w, x['lab'] + ' ' + d) or offensive(w, d, x['lab']): continue
            ex = [y for y in x['ex'] if not (religious('', y[1]) or offensive('', y[1]) or any(religious(t) or offensive(t) for t in re.findall(r'[а-яёәөүҗңһ]+', y[0].lower())))]
            ss.append(dict(n=len(ss) + 1, lab=xl, d=d[:200], ex=ex[:2]))
        if ss: hom.append(dict(pos=e['pos'], senses=ss))
    first_all = ' '.join(gt_clean(x['d']) + ' ' + x['lab'] for e in es for x in e['senses'][:1])
    if religious(w, first_all) or offensive(w, first_all): BANNED.add(w); continue
    if not hom: continue
    g = hom[0]['senses'][0]['d']; lab = hom[0]['senses'][0]['lab']
    loan = bool(LOAN_LET.search(w)) or w in re.findall(r'[а-яё]+', g.lower())
    special = bool(re.match(r'^(?:чаще|и прич|прич|от |в роли|см\.|то же|форма|деепр|употр|с послел|мн\.|ед\.)', g)) or any(x in lab for x in SPECIAL) or bool(re.search(r'(?:разг|уст|диал|прост|бран|груб)\.?', lab))
    UD[w] = dict(g=g, loan=loan, special=special, f=freq.get(w, 0),
                 card=dict(stress='', gram=', '.join(sorted({POS_RU[e['pos']] for e in hom})), hill='', hom=hom, extra=[], src='gt'))
    GT_ADDED += 1
print('GiellaLT dict-kpv-rus: added', GT_ADDED, 'headwords', file=sys.stderr)
gloss_fix = json.load(open(f'{S}/ru_gloss_fix.json')) if os.path.exists(f'{S}/ru_gloss_fix.json') else {}
for w, g in gloss_fix.items():   # hand-corrected first glosses (Wiktionary's first sense is sometimes rare or odd)
    if w in UD:
        UD[w]['g'] = g; UD[w]['card']['hom'][0]['senses'][0]['d'] = g
UD_COMPLETE = True

def gloss(w):
    if w in UD and UD[w]['g']: return UD[w]['g'][:90], 'ud'
    if w in form_of and form_of[w] in UD and UD[form_of[w]]['g']:
        return ('форма слова ' + form_of[w] + ' — ' + UD[form_of[w]]['g'])[:90], 'ru'
    if w in wk_en: return '; '.join(wk_en[w][:2])[:80], 'en'
    return None, None

# ---------- lexicon ----------
lex = {}
for w, v in UD.items():
    lex[w] = dict(f=v['f'], b=v['loan'] or v['special'] or not v['g'])
for w in wk_en:            # extra headwords from en.wiktionary: bonus only
    if w in lex or w in BANNED or not LET.match(w): continue
    if religious(w, ' '.join(wk_en[w])) or offensive(w, ' '.join(wk_en[w])): BANNED.add(w); continue
    lex[w] = dict(f=freq.get(w, 0), b=True)
for fw, lw in form_of.items():   # attested inflected forms of dictionary words: bonus only
    if fw in lex or lw not in UD or fw in BANNED or freq.get(fw, 0) < 30: continue
    if religious(fw) or offensive(fw): continue
    lex[fw] = dict(f=freq.get(fw, 0), b=True)

def score(w):
    e = lex[w]; f = e['f']
    return (0 if f <= 0 else 4 * len(str(int(f)))) + min(f, 3000) / 30 + (6 if w in UD else 0) + (3 if w in UD and UD[w]['card']['hom'][0]['senses'][0]['ex'] else 0)
grid_words = {w for w, e in lex.items() if not e['b'] and e['f'] >= 3}
bonus_words = set(lex) | grid_words
print('lexicon', len(lex), 'grid', len(grid_words), 'bonus', len(bonus_words), 'banned', len(BANNED), file=sys.stderr)
_cc = {}
def can_make(word, pool):
    c = _cc.get(word)
    if c is None: c = _cc[word] = collections.Counter(word)
    return all(pool[k] >= v for k, v in c.items())

# --- crossword layout ---
def layout(words, tries=300):
    best = None
    for t in range(tries):
        ws = sorted(words, key=lambda w: -len(w)) if t == 0 else random.sample(words, len(words))
        if t and random.random() < .5: ws = sorted(ws, key=lambda w: -len(w) + random.random() * 2)
        grid = {}; placed = []
        def fits(w, r, c, d):
            dr, dc = (0, 1) if d == 'h' else (1, 0)
            if (r - dr, c - dc) in grid or (r + dr * len(w), c + dc * len(w)) in grid: return False
            cross = 0
            for i, ch in enumerate(w):
                p = (r + dr * i, c + dc * i)
                if p in grid:
                    if grid[p][0] != ch or grid[p][1] == d: return False
                    cross += 1
                else:
                    n1 = (p[0] + dc, p[1] + dr); n2 = (p[0] - dc, p[1] - dr)
                    if n1 in grid or n2 in grid: return False
            return cross
        def put(w, r, c, d):
            dr, dc = (0, 1) if d == 'h' else (1, 0)
            for i, ch in enumerate(w):
                p = (r + dr * i, c + dc * i)
                grid[p] = (ch, 'x' if p in grid else d)
            placed.append((w, r, c, d))
        put(ws[0], 0, 0, 'h')
        left = ws[1:]; progress = True
        while left and progress:
            progress = False
            for w in list(left):
                opts = []
                for (pr, pc), (ch, pd) in list(grid.items()):
                    if pd == 'x': continue
                    nd = 'v' if pd == 'h' else 'h'
                    for i, wc in enumerate(w):
                        if wc != ch: continue
                        r, c = (pr - i, pc) if nd == 'v' else (pr, pc - i)
                        x = fits(w, r, c, nd)
                        if x: opts.append((x, random.random(), r, c, nd))
                if opts:
                    opts.sort(reverse=True); _, _, r, c, d = opts[0]
                    put(w, r, c, d); left.remove(w); progress = True
        rs = [p[0] for p in grid]; cs = [p[1] for p in grid]
        h = max(rs) - min(rs) + 1; wd = max(cs) - min(cs) + 1
        sc = len(placed) * 100 - abs(h - wd) * 3 - h * wd * 0.5 - max(0, wd - 10) * 50 - max(0, h - 10) * 50
        if best is None or sc > best[0]:
            mr, mc = min(rs), min(cs)
            best = (sc, [(w, r - mr, c - mc, d) for w, r, c, d in placed], h, wd)
        if len(placed) == len(words) and t > 60: break
    return best

