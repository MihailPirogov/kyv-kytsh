#!/usr/bin/env python3
"""Stage (NOT publish) the public pages for «Кыв кытш» on pirogovlab.ru.
Input: read-only copies of live pages in site_stage/live/ (scp from the server; Сүз дөньясы / Чӑваш сӑмахӗ pages are templates only).
Output: site_stage/out/ — kyv-kytsh-igra/, en/kyv-kytsh-igra/, blog/DATE-kyv-kytsh/, en/blog/DATE-kyv-kytsh/ (+ img, blog media)
and patched copies of index.html, en/index.html, blog/index.html, en/blog/index.html, blog/rss.xml, en/blog/rss.xml, sitemap.xml.
The game itself (/kyv-kytsh/, /kyv-kytsh/privacy/) stays noindex and is NOT added to sitemap.
Landing keeps the shared header/footer/cookie banner of the template; the «Как играть» block (rsya:about) is written anew."""
import re, os, html, sys, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = ROOT + '/site_stage/live/'; O = ROOT + '/site_stage/out/'
DATE = sys.argv[1] if len(sys.argv) > 1 else '2026-10-22'
Y, M, D = DATE.split('-'); MRU = ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря'][int(M)-1]
MEN = ['January','February','March','April','May','June','July','August','September','October','November','December'][int(M)-1]
DRU = f'{int(D)} {MRU} {Y}'; DEN = f'{MEN} {int(D)}, {Y}'
RFC = datetime.date(int(Y), int(M), int(D)).strftime('%a, %d %b %Y') + ' 14:00:00 +0300'
SLUG = f'{DATE}-kyv-kytsh'; VER = '1.0.0'
APK = '/kyv-kytsh/kyv-kytsh.apk'; SIZE_RU = '27 МБ'; SIZE_EN = '27 MB'
GAME = '/kyv-kytsh/'; PRIV = '/kyv-kytsh/privacy/'
RU_P = 'https://pirogovlab.ru/kyv-kytsh-igra/'; EN_P = 'https://pirogovlab.ru/en/kyv-kytsh-igra/'
IMG = '/kyv-kytsh-igra/img/'; OG = 'https://pirogovlab.ru' + IMG + 'og-kyv-kytsh.jpg'
e = html.escape
def rd(p): return open(L + p, encoding='utf-8').read()
def wr(p, s):
    os.makedirs(os.path.dirname(O + p), exist_ok=True); open(O + p, 'w', encoding='utf-8').write(s)
def sub1(pat, rep, s):
    n, k = re.subn(pat, lambda m: rep, s, count=1); assert k == 1, pat; return n
def head(s, title, desc, canon, ogt, ogd, ogimg, ru, en):
    s = sub1(r'<title>.*?</title>', f'<title>{e(title)}</title>', s)
    s = sub1(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(desc)}">', s)
    s = sub1(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{canon}">', s)
    s = sub1(r'<link rel="alternate" hreflang="ru" href="[^"]*">', f'<link rel="alternate" hreflang="ru" href="{ru}">', s)
    s = sub1(r'<link rel="alternate" hreflang="en" href="[^"]*">', f'<link rel="alternate" hreflang="en" href="{en}">', s)
    s = sub1(r'<link rel="alternate" hreflang="x-default" href="[^"]*">', f'<link rel="alternate" hreflang="x-default" href="{ru}">', s)
    s = sub1(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{e(ogt)}">', s)
    s = sub1(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{e(ogd)}">', s)
    s = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{canon}">', s, count=1)
    s = sub1(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{ogimg}">', s)
    s = sub1(r'<meta name="twitter:image" content="[^"]*">', f'<meta name="twitter:image" content="{ogimg}">', s)
    return s
def rename(s):
    for a, b in [('suz-donyasy', 'kyv-kytsh'), ('suzdonyasy', 'kyvkytsh'), ('Сүз дөньясы', 'Кыв кытш'), ('Süz Dönyası', 'Kyv kytsh'),
                 ('chavash-samakhe', 'kyv-kytsh'), ('chavashsamakhe', 'kyvkytsh'), ('Чӑваш сӑмахӗ', 'Кыв кытш'), ('Chăvash Sămakhĕ', 'Kyv kytsh')]: s = s.replace(a, b)
    return s
def split(s): a = s.index('<main'); b = s.index('</main>') + 7; return s[:a], s[b:]
GP_SVG = '<svg viewBox="0 0 24 26" aria-hidden="true" width="26" height="28"><path fill="#00d7fe" d="M1 .6 13.4 13 1 25.4C.6 25.2.4 24.7.4 24.1V1.9C.4 1.3.6.8 1 .6z"/><path fill="#ffce00" d="m17.5 8.9 4.3 2.4c1.3.8 1.3 2 0 2.8l-4.3 2.4L13.4 13z"/><path fill="#ff3a44" d="M17.5 17.1 13.4 13 1 25.4c.5.4 1.2.4 2 0z"/><path fill="#00f076" d="M17.5 8.9 3 .6C2.2.2 1.5.2 1 .6L13.4 13z"/></svg>'
def stores(lang):
    t = (lambda ru, en: ru if lang == 'ru' else en)
    return ('<!-- PLACEHOLDER stores: set href and remove "hidden" when each listing is live -->\n      <div class="stores-row">'
      f'<a class="store rs" href="#rustore" rel="noopener" hidden><i>R</i><span><small>{t("Скачать в","Get it on")}</small><b>RuStore</b></span></a>'
      f'<a class="store gp" href="#google-play" rel="noopener" hidden>{GP_SVG}<span><small>{t("Доступно в","Get it on")}</small><b>Google Play</b></span></a>'
      f'<a class="store yg" href="#yandex-games" rel="noopener" hidden><i>Я</i><span><small>{t("Играть в","Play on")}</small><b>{t("Яндекс Играх","Yandex Games")}</b></span></a></div>')
SH = {'ru': [('game','Кроссворд и круг с буквами'),('card','Карточка слова с переводом'),('map','Карта: 50 глав'),('daily','Задача дня'),('spin','Колесо удачи'),('home','Главный экран'),('tutorial','Обучение при первом запуске')],
      'en': [('game','Crossword and the letter wheel'),('card','Word card with translation'),('map','Map: 50 chapters'),('daily','Daily puzzle'),('spin','Fortune wheel'),('home','Home screen'),('tutorial','First-launch tutorial')]}
def gal(lang): return '<div class="gal">' + ''.join(f'<figure class="shot"><img src="{IMG}screen-{k}.webp" width="540" height="960" loading="lazy" alt="{c}"><figcaption>{c}</figcaption></figure>' for k, c in SH[lang]) + '</div>'

def landing(lang):
    s = rd(('en/' if lang == 'en' else '') + 'suz-donyasy-igra/index.html'); pre, post = split(s); pre, post = rename(pre), rename(post)
    if lang == 'ru':
        pre = head(pre, 'Кыв кытш — словесная игра на коми языке | Pirogov Lab',
          'Кыв кытш («Круг слов») — бесплатная словесная головоломка: составляйте коми слова из букв, 500 уровней в 50 главах, перевод каждого слова на русский. Игра в браузере и на Android.',
          RU_P, 'Кыв кытш — словесная игра на коми языке', 'Соединяйте буквы, составляйте коми слова и заполняйте кроссворд. 500 уровней, карточки слов с переводом, задача дня и колесо удачи.', OG, RU_P, EN_P)
        main = f'''<main class="wrap">
  <header>
    <div>
      <img class="applogo" src="{IMG}logo.webp" width="256" height="256" alt="Кыв кытш">
      <p class="eyebrow"><span>Коми кыв · Android · Браузер</span></p>
      <h1>Кыв кытш — круг коми слов</h1>
      <p class="lead">Словесная головоломка на <b>коми языке</b>: соединяйте буквы на круге, составляйте слова и заполняйте кроссворд. <b>500 уровней</b>, а у каждого слова — карточка с переводом на русский.</p>
      <div class="dl"><a class="btn" href="{GAME}">▶ Играть в браузере</a><a class="btn ghost" href="{APK}" download>⬇ Скачать APK ({VER}, {SIZE_RU})</a></div>
      {stores('ru')}
      <div class="meta"><span class="pill">Версия {VER}</span><span class="pill">{DRU}</span><span class="pill">Android 7.0+</span><span class="pill">Бесплатно</span></div>
    </div>
    <figure class="hero-app"><div class="tilt"><img src="{IMG}screen-game.webp" width="540" height="960" alt="Кыв кытш — уровень с кроссвордом и кругом букв" fetchpriority="high"></div></figure>
  </header>
  <hr class="rule" style="margin-top:1rem">
  <!-- rsya:about:start --><section aria-labelledby="ab"><h2 id="ab">Как играть в «Кыв кытш»</h2><div class="card" style="text-align:left"><p>Соединяйте буквы на круге в слова: правильное слово сразу встаёт в кроссворд. Уровень пройден, когда все клетки заполнены, а дополнительные найденные слова попадают в копилку бонусов.</p><p>Коми буквы ӧ и і уже стоят на колесе, поэтому их не нужно искать на клавиатуре. Обращайте на них внимание: ӧ и о, і и и в коми языке — разные звуки, и от них зависит смысл слова.</p><p>Нажмите на любое найденное слово, чтобы увидеть перевод на русский и примеры, — так за несколько уровней набирается небольшой личный словарь коми слов.</p></div></section><!-- rsya:about:end -->
  <section aria-labelledby="f"><h2 id="f">Возможности</h2><div class="card"><ul style="padding-left:1.2rem;margin:0">
    <li><b>500 уровней в 50 главах</b> — Видз, Вӧр, Парма, Эжва, Изьва, Печора, Кӧр, Мойд, Сер…; у каждой главы свой живописный фон с северной природой</li>
    <li><b>Коми буквы Ӧ и І</b> — прямо на колесе, ничего набирать не нужно</li>
    <li><b>Карточки слов</b> — нажмите на найденное слово: перевод на русский, значения и примеры</li>
    <li><b>«Мой словарь»</b> — все выученные слова в одном месте; бонусные слова попадают в копилку</li>
    <li><b>Каждый день</b> — задача дня, слово дня, ежедневная награда, задания, колесо удачи и достижения</li>
    <li>Подсказки: 💡 открыть букву, 🎯 открыть слово, ⟳ перемешать; короткое обучение при первом запуске; работает <b>без интернета</b></li>
  </ul></div></section>
  <section aria-labelledby="s"><h2 id="s">Скриншоты</h2><figure class="shot" style="margin-bottom:1.5rem"><img src="{IMG}feature-graphic.webp" width="1024" height="500" loading="lazy" alt="Кыв кытш — коми кывъяс"></figure>
  {gal('ru')}
  <div class="wide"><figure class="shot"><img src="{IMG}desktop-game.webp" width="1280" height="720" loading="lazy" alt="Версия для компьютера"><figcaption>В браузере на компьютере</figcaption></figure><figure class="shot"><img src="{IMG}desktop-card.webp" width="1280" height="720" loading="lazy" alt="Карточка слова на компьютере"><figcaption>Карточка слова</figcaption></figure></div></section>
  <section aria-labelledby="i"><h2 id="i">Где играть</h2><div class="card"><p style="margin:0">Прямо сейчас — <a href="{GAME}">в браузере</a> на телефоне или компьютере (прогресс сохраняется на устройстве) или на Android: скачайте <a href="{APK}" download>kyv-kytsh.apk</a> ({VER}, {SIZE_RU}), откройте файл и разрешите установку из этого источника. Скоро «Кыв кытш» появится в RuStore, Google Play и Яндекс Играх.</p></div></section>
  <section aria-labelledby="src"><h2 id="src">Словарь</h2><div class="card"><ul class="src" style="padding-left:1.2rem;margin:0"><li>Слова, переводы и примеры — коми-русский словарь <a href="https://github.com/giellalt/dict-kpv-rus" target="_blank" rel="noopener">GiellaLT / Giellatekno</a> (UiT, CC BY 4.0) и коми статьи <a href="https://ru.wiktionary.org" target="_blank" rel="noopener">Викисловаря</a> (CC BY-SA 4.0; данные Wiktextract / kaikki.org)</li><li>Частоты слов — коми Википедия</li></ul>
  <p class="note">В мобильных версиях будет ненавязчивая реклама (после обучения, между уровнями и по желанию — за подсказку). <a href="{PRIV}">Политика конфиденциальности</a>.</p></div></section>
  <aside class="callout" role="note" style="margin-top:3rem"><div class="callout-ico" aria-hidden="true">✦</div><p>Проект лаборатории <a href="https://pirogovlab.ru">PirogovLab</a>. Нашли ошибку в слове или переводе? Напишите в <a href="/contacts/">Telegram</a>.</p></aside>
</main>'''
        wr('kyv-kytsh-igra/index.html', pre + main + post)
    else:
        pre = head(pre, 'Kyv kytsh — a word game in the Komi language | Pirogov Lab',
          'Kyv kytsh (“Word Circle”) is a free word puzzle: build Komi words from letters, 500 levels in 50 chapters, a Russian translation for every word. Play in the browser or on Android.',
          EN_P, 'Kyv kytsh — a word game in the Komi language', 'Connect letters, build Komi words and fill the crossword. 500 levels, word cards with translations, a daily puzzle and a fortune wheel.', OG, RU_P, EN_P)
        main = f'''<main class="wrap">
  <header>
    <div>
      <img class="applogo" src="{IMG}logo.webp" width="256" height="256" alt="Kyv kytsh">
      <p class="eyebrow"><span>Komi language · Android · Browser</span></p>
      <h1>Kyv kytsh — a circle of Komi words</h1>
      <p class="lead">A word puzzle in the <b>Komi language</b>: connect letters on the wheel, build words and fill the crossword. <b>500 levels</b>, and every word has a card with its Russian translation.</p>
      <div class="dl"><a class="btn" href="{GAME}" hreflang="ru">▶ Play in the browser</a><a class="btn ghost" href="{APK}" download>⬇ Download APK ({VER}, {SIZE_EN})</a></div>
      {stores('en')}
      <div class="meta"><span class="pill">Version {VER}</span><span class="pill">{DEN}</span><span class="pill">Android 7.0+</span><span class="pill">Free</span></div>
    </div>
    <figure class="hero-app"><div class="tilt"><img src="{IMG}screen-game.webp" width="540" height="960" alt="Kyv kytsh — a level with the crossword and the letter wheel" fetchpriority="high"></div></figure>
  </header>
  <hr class="rule" style="margin-top:1rem">
  <!-- rsya:about:start --><section aria-labelledby="ab"><h2 id="ab">How to play Kyv kytsh</h2><div class="card" style="text-align:left"><p>Connect letters on the wheel to form words; a correct word drops into the crossword. The level is done when every cell is filled, and extra words go to the bonus jar.</p><p>The Komi letters ӧ and і are on the wheel, so there is no need to hunt for them on a keyboard. Tap any found word for its Russian translation and examples.</p></div></section><!-- rsya:about:end -->
  <section aria-labelledby="f"><h2 id="f">Features</h2><div class="card"><ul style="padding-left:1.2rem;margin:0">
    <li><b>500 levels in 50 chapters</b>, each with its own scenic background of northern nature: meadows, taiga, the Vychegda and Pechora rivers, reindeer</li>
    <li><b>Komi letters Ӧ and І</b> right on the wheel, no typing needed</li>
    <li><b>Word cards</b>: tap a found word to see its Russian translation, meanings and examples</li>
    <li><b>“My dictionary”</b>: every word you have learned; bonus words go into a jar</li>
    <li><b>Every day</b>: a daily puzzle, a word of the day, a daily reward, quests, a fortune wheel and achievements</li>
    <li>Hints: 💡 reveal a letter, 🎯 reveal a word, ⟳ shuffle; a short tutorial; works <b>offline</b>; the interface is in Russian</li>
  </ul></div></section>
  <section aria-labelledby="s"><h2 id="s">Screenshots</h2><figure class="shot" style="margin-bottom:1.5rem"><img src="{IMG}feature-graphic.webp" width="1024" height="500" loading="lazy" alt="Kyv kytsh"></figure>
  {gal('en')}
  <div class="wide"><figure class="shot"><img src="{IMG}desktop-game.webp" width="1280" height="720" loading="lazy" alt="Desktop browser version"><figcaption>In a desktop browser</figcaption></figure><figure class="shot"><img src="{IMG}desktop-card.webp" width="1280" height="720" loading="lazy" alt="A word card on desktop"><figcaption>A word card</figcaption></figure></div></section>
  <section aria-labelledby="i"><h2 id="i">Where to play</h2><div class="card"><p style="margin:0">Right now: <a href="{GAME}" hreflang="ru">in the browser</a> on a phone or computer (progress is saved on the device), or on Android: download <a href="{APK}" download>kyv-kytsh.apk</a> ({VER}, {SIZE_EN}), open it and allow installs from this source. RuStore, Google Play and Yandex Games are coming soon.</p></div></section>
  <section aria-labelledby="src"><h2 id="src">Dictionary</h2><div class="card"><ul class="src" style="padding-left:1.2rem;margin:0"><li>Words, translations and examples: the <a href="https://github.com/giellalt/dict-kpv-rus" target="_blank" rel="noopener">GiellaLT / Giellatekno</a> Komi–Russian dictionary (UiT, CC BY 4.0) and Komi entries of <a href="https://ru.wiktionary.org" target="_blank" rel="noopener">Wiktionary</a> (CC BY-SA 4.0)</li><li>Word frequencies: Komi Wikipedia</li></ul>
  <p class="note">Mobile versions will show unobtrusive ads (after the tutorial, between levels and, if you choose, for a hint). <a href="{PRIV}">Privacy policy</a> (in Russian).</p></div></section>
  <aside class="callout" role="note" style="margin-top:3rem"><div class="callout-ico" aria-hidden="true">✦</div><p>A <a href="https://pirogovlab.ru/en/">PirogovLab</a> project. Found a mistake in a word or translation? Message me on <a href="/en/contacts/">Telegram</a>.</p></aside>
</main>'''
        wr('en/kyv-kytsh-igra/index.html', pre + main + post)

def blogpost(lang):
    s = rd(('en/' if lang == 'en' else '') + 'blog/2026-10-20-chavash-samakhe/index.html'); pre, post = split(s); pre, post = rename(pre), rename(post)
    img = 'https://pirogovlab.ru/blog/media/kyv-kytsh.jpg'; ru_u = f'https://pirogovlab.ru/blog/{SLUG}/'; en_u = f'https://pirogovlab.ru/en/blog/{SLUG}/'
    if lang == 'ru':
        T = '«Кыв кытш»: словесная игра на коми языке'
        DS = 'Сделал «Кыв кытш» — словесную головоломку на коми языке: 500 уровней, перевод каждого слова, задача дня и колесо удачи. Играть можно в браузере и на Android.'
        pre = head(pre, T + ' | Pirogov Lab', DS, ru_u, T, DS, img, ru_u, en_u)
        main = f'''<main class="wrap">
<article class="full">
  <p class="eyebrow"><a href="/blog/">Микроблог</a></p>
  <h1>{T}</h1>
  <time class="date" datetime="{DATE}T14:00:00+03:00">{DRU}</time>
  <figure class="media"><img src="/blog/media/kyv-kytsh.jpg" width="1200" height="630" alt="{T}"></figure>
  <div class="body">
<p>Следующий язык в серии словесных игр — <b>коми</b>. Встречайте <b>«Кыв кытш»</b> («Круг слов»): соединяйте буквы на круге, составляйте коми слова и заполняйте ими кроссворд.</p>
<h2>Что внутри</h2>
<ul>
<li><b>500 уровней в 50 главах</b>: Видз (луг), Вӧр (лес), Парма (тайга), Эжва (Вычегда), Изьва (Ижма), Печора, Кӧр (олень), Мойд (сказка), Сер (узор)… У каждой главы свой фон с северной природой.</li>
<li>Буквы <b>Ӧ и І</b> прямо на колесе, а вокруг — красно-белый коми орнамент.</li>
<li><b>Карточки слов</b>: нажмите на найденное слово — перевод на русский, значения и примеры. Выученные слова собираются в «Мой словарь».</li>
<li><b>Каждый день</b> — задача дня, слово дня, ежедневная награда, задания и колесо удачи.</li>
<li>Подсказки, бонусные слова и короткое обучение при первом запуске. Можно играть <b>без интернета</b>.</li>
</ul>
<p>Слова, переводы и примеры взяты из открытого коми-русского словаря GiellaLT / Giellatekno (CC BY 4.0) и Викисловаря (CC BY-SA 4.0), порядок уровней — по частоте слов в коми Википедии: сначала простые, потом посложнее. Игра подойдёт и тем, кто говорит по-коми, и тем, кто только начинает учить язык.</p>
<p>Играть можно <b>прямо в браузере</b> или поставить APK на Android. Скоро игра появится в RuStore, Google Play и Яндекс Играх.</p>
<p>Нашли ошибку в слове или переводе? Напишите мне в <a href="/contacts/">Telegram</a> — буду исправлять. Аттьӧ!</p>
  </div>
  <div class="stores"><a class="btn" href="{GAME}">▶ Играть в браузере</a></div>
  <div class="meta"><span class="pill">Версия {VER}</span><a class="pill" href="https://pirogovlab.ru{APK}" download>⬇ Android: скачать APK ({SIZE_RU})</a><a class="pill" href="/kyv-kytsh-igra/">Страница игры</a><span class="pill">Бесплатно</span></div>
  <a class="proj" href="/kyv-kytsh-igra/"><img src="{IMG}kartochka-kyv-kytsh.webp" width="480" height="320" alt=""><div><b>Кыв кытш</b><span>Страница игры: возможности, скриншоты, где играть</span></div><span class="go" aria-hidden="true">→</span></a>
  <a class="backlink" href="/blog/">← Все записи</a>
</article>
</main>'''
        wr(f'blog/{SLUG}/index.html', pre + main + post)
    else:
        T = 'Kyv kytsh: a word game in the Komi language'
        DS = 'I made Kyv kytsh, a word puzzle in Komi: 500 levels, a translation for every word, a daily puzzle and a fortune wheel. Play in the browser or on Android.'
        pre = head(pre, T + ' | Pirogov Lab', DS, en_u, T, DS, img, ru_u, en_u)
        main = f'''<main class="wrap">
<article class="full">
  <p class="eyebrow"><a href="/en/blog/">Microblog</a></p>
  <h1>{T}</h1>
  <time class="date" datetime="{DATE}T14:00:00+03:00">{DEN}</time>
  <figure class="media"><img src="/blog/media/kyv-kytsh.jpg" width="1200" height="630" alt="{T}"></figure>
  <div class="body">
<p>The next language in my series of word games is <b>Komi</b>. Meet <b>Kyv kytsh</b> (“Word Circle”): connect letters on the wheel, build Komi words and fill the crossword with them.</p>
<h2>What's inside</h2>
<ul>
<li><b>500 levels in 50 chapters</b>, each with its own background of northern nature: meadows, taiga, the Vychegda and Pechora rivers, reindeer.</li>
<li>The letters <b>Ӧ and І</b> right on the wheel, framed by a red-and-white Komi ornament.</li>
<li><b>Word cards</b>: tap a found word to see its Russian translation, meanings and examples. Learned words go into “My dictionary”.</li>
<li><b>Every day</b>: a daily puzzle, a word of the day, a daily reward, quests and a fortune wheel.</li>
<li>Hints, bonus words and a short tutorial on first launch. Works <b>offline</b>.</li>
</ul>
<p>Words and translations come from the open GiellaLT / Giellatekno Komi–Russian dictionary (CC BY 4.0) and Wiktionary (CC BY-SA 4.0). You can <b>play right in the browser</b> or install the APK; RuStore, Google Play and Yandex Games are coming soon. The interface is in Russian.</p>
<p>Found a mistake in a word or translation? Message me on <a href="/en/contacts/">Telegram</a>.</p>
  </div>
  <div class="stores"><a class="btn" href="{GAME}" hreflang="ru">▶ Play in the browser</a></div>
  <div class="meta"><span class="pill">Version {VER}</span><a class="pill" href="https://pirogovlab.ru{APK}" download>⬇ Android: download APK ({SIZE_EN})</a><a class="pill" href="/en/kyv-kytsh-igra/">Game page</a><span class="pill">Free</span></div>
  <a class="proj" href="/en/kyv-kytsh-igra/"><img src="{IMG}kartochka-kyv-kytsh.webp" width="480" height="320" alt=""><div><b>Kyv kytsh</b><span>Game page: features, screenshots, where to play</span></div><span class="go" aria-hidden="true">→</span></a>
  <a class="backlink" href="/en/blog/">← All posts</a>
</article>
</main>'''
        wr(f'en/blog/{SLUG}/index.html', pre + main + post)

def patch(rel, fn):
    s = rd(rel); n = fn(s); assert n != s, rel; wr(rel, n)
def home(lang):
    def f(s):
        en = lang == 'en'; p = '/en' if en else ''
        mb = (f'<a class="mbf" href="{p}/blog/{SLUG}/"><img src="/blog/media/kyv-kytsh-thumb.webp" width="960" height="540" alt=""><div><time datetime="{DATE}">{DEN if en else DRU}</time>'
              + ('<b>Kyv kytsh: a word game in Komi</b><span>Connect letters, build Komi words and fill the crossword: 500 levels and a translation for every word</span>' if en else
                 '<b>«Кыв кытш»: словесная игра на коми языке</b><span>Соединяйте буквы, составляйте коми слова и заполняйте кроссворд: 500 уровней и перевод каждого слова</span>') + '</div></a>\n      ')
        i = s.index('<a class="mbf"'); n0 = len(re.findall(r'      <a class="mbf" href=', s)); s = s[:i] + mb + s[i:]
        items = list(re.finditer(r'      <a class="mbf" href="[^"]*".*?</a>\n', s, re.S))
        if len(items) > n0: last = items[-1]; s = s[:last.start()] + s[last.end():]   # keep feed length
        pj = (f'<a class="proj" href="{p}/kyv-kytsh-igra/"><img src="{IMG}kartochka-kyv-kytsh.webp" width="480" height="320" alt="'
              + ('Kyv kytsh — a word game in the Komi language"><div><b>Kyv kytsh — a circle of Komi words</b><span>A word puzzle in Komi: 500 levels and a translation for every word</span>' if en else
                 'Кыв кытш — словесная игра на коми языке"><div><b>Кыв кытш — круг коми слов</b><span>Словесная головоломка на коми языке: 500 уровней и перевод каждого слова</span>')
              + '</div><span class="go" aria-hidden="true">→</span></a>\n  ')
        i = s.index('<a class="proj" href="' + p + '/'); return s[:i] + pj + s[i:]
    return f
def blog_idx(lang):
    def f(s):
        if lang == 'ru':
            a = f'''  <article class="card post">
    <time class="date" datetime="{DATE}T14:00:00+03:00">{DRU}</time>
    <h2><a href="/blog/{SLUG}/">«Кыв кытш»: словесная игра на коми языке</a></h2>
    <figure class="media"><img src="/blog/media/kyv-kytsh.jpg" width="1200" height="630" alt="Кыв кытш — круг коми слов" loading="lazy"></figure>
    <p>Словесная головоломка на коми языке: соединяйте буквы, составляйте слова и заполняйте кроссворд. 500 уровней в 50 главах, перевод каждого слова, задача дня и колесо удачи. Играть можно в браузере и на Android, скоро — RuStore, Google Play и Яндекс Игры.</p>
    <a class="more" href="/blog/{SLUG}/">Читать полностью →</a>
  </article>
'''
        else:
            a = f'''  <article class="card post">
    <time class="date" datetime="{DATE}T14:00:00+03:00">{DEN}</time>
    <h2><a href="/en/blog/{SLUG}/">Kyv kytsh: a word game in the Komi language</a></h2>
    <figure class="media"><img src="/blog/media/kyv-kytsh.jpg" width="1200" height="630" alt="Kyv kytsh — a circle of Komi words" loading="lazy"></figure>
    <p>A word puzzle in Komi: connect letters, build words and fill the crossword. 500 levels in 50 chapters, a translation for every word, a daily puzzle and a fortune wheel. Play in the browser or on Android; RuStore, Google Play and Yandex Games coming soon.</p>
    <a class="more" href="/en/blog/{SLUG}/">Read more →</a>
  </article>
'''
        assert '  <div class="feed">\n' in s; return s.replace('  <div class="feed">\n', '  <div class="feed">\n' + a, 1)
    return f
def rss(lang):
    def f(s):
        base = f'https://pirogovlab.ru/{"en/" if lang == "en" else ""}blog/{SLUG}/'
        t = '«Кыв кытш»: словесная игра на коми языке' if lang == 'ru' else 'Kyv kytsh: a word game in the Komi language'
        d = ('Словесная головоломка на коми языке: 500 уровней, перевод каждого слова, задача дня и колесо удачи.' if lang == 'ru'
             else 'A word puzzle in Komi: 500 levels, a translation for every word, a daily puzzle and a fortune wheel.')
        item = f'    <item>\n      <title>{t}</title>\n      <link>{base}</link>\n      <guid isPermaLink="true">{base}</guid>\n      <pubDate>{RFC}</pubDate>\n      <description>{d}</description>\n    </item>\n'
        s = re.sub(r'<lastBuildDate>.*?</lastBuildDate>', f'<lastBuildDate>{RFC}</lastBuildDate>', s, count=1)
        i = s.index('    <item>'); return s[:i] + item + s[i:]
    return f
def sitemap(s):
    # landings + blog posts only; the game /kyv-kytsh/ and its privacy page stay OUT of sitemap (noindex)
    add = ''.join(f'  <url><loc>https://pirogovlab.ru/{u}</loc><lastmod>{DATE}</lastmod></url>\n' for u in
        ['kyv-kytsh-igra/', 'en/kyv-kytsh-igra/', f'blog/{SLUG}/', f'en/blog/{SLUG}/'])
    for u in ['', 'en/', 'blog/', 'en/blog/']:
        s = re.sub(rf'(<url><loc>https://pirogovlab.ru/{re.escape(u)}</loc><lastmod>)[^<]*', rf'\g<1>{DATE}', s)
    return s.replace('</urlset>', add + '</urlset>')

landing('ru'); landing('en'); blogpost('ru'); blogpost('en')
patch('index.html', home('ru')); patch('en/index.html', home('en'))
patch('blog/index.html', blog_idx('ru')); patch('en/blog/index.html', blog_idx('en'))
patch('blog/rss.xml', rss('ru')); patch('en/blog/rss.xml', rss('en')); patch('sitemap.xml', sitemap)
print('staged ->', O, 'slug', SLUG)
