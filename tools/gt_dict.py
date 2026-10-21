"""Giellatekno / GiellaLT dict-kpv-rus (CC BY 4.0, https://github.com/giellalt/dict-kpv-rus) -> {lemma: [entry...]}.
entry = dict(pos, senses=[dict(lab, d, ex=[[kpv, rus, '']])], range) ; dialect/obsolete-ranged senses are flagged."""
import re, glob, os, xml.etree.ElementTree as ET
POS = {'N': 'noun', 'V': 'verb', 'A': 'adj', 'Adv': 'adv', 'Num': 'num', 'Pron': 'pron'}
NORM = str.maketrans({'i': 'і', 'ö': 'ӧ', 'I': 'І', 'Ö': 'Ӧ'})
def text(el):
    if el is None: return '', ''
    labs = [a.text.strip() for a in el.iter('acronym') if a.text]
    s = ''.join(el.itertext()); s = re.sub(r'\s+', ' ', s).strip(' ;,')
    s = re.sub(r'смотри также:.*$', '', s).strip(' ;,(')
    return s, ' '.join(labs)
def load(src):
    out = {}
    for f in sorted(glob.glob(os.path.join(src, 'src', '*_kpvrus.xml'))):
        pos_f = os.path.basename(f).split('_')[0]
        if pos_f not in POS: continue
        for e in ET.parse(f).getroot().iter('e'):
            l = e.find('lg/l')
            if l is None or not l.text: continue
            w = l.text.strip().lower().translate(NORM)
            senses = []
            for mg in e.findall('mg'):
                rng = ' '.join(r.get('range_space', '') + ':' + (r.text or '') for r in mg.iter('r'))
                for tg in mg.findall('tg'):
                    for t in tg.findall('t'):
                        d, lab = text(t)
                        for a in t.iter('acronym'):
                            if a.text and d.startswith(a.text.strip()): d = d[len(a.text.strip()):].strip()
                        if not d: continue
                        ex = []
                        for xg in mg.findall('xg'):
                            x, _ = text(xg.find('x')); xt, _ = text(xg.find('xt'))
                            if x and xt and len(x) < 120: ex.append([x, xt, ''])
                        senses.append(dict(lab=lab, d=d, ex=ex[:2], rng=rng))
                        break
            if senses: out.setdefault(w, []).append(dict(pos=POS[pos_f], senses=senses))
    return out
if __name__ == '__main__':
    import sys, collections
    D = load(sys.argv[1]); print(len(D))
    rng = collections.Counter(s['rng'] for es in D.values() for e in es for s in e['senses']); print(rng.most_common(15))
    for w in ['ва', 'вӧр', 'кань', 'шонді', 'керка', 'ен', 'вичко', 'мича', 'ворсны']: print(w, [(e['pos'], [(s['lab'], s['d'][:40], s['rng']) for s in e['senses'][:2]]) for e in D.get(w, [])])
