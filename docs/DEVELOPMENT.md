# Кыв кытш  — словесная игра на коми (коми-зырянском) языке

Механика как Words of Wonders: круг букв + кроссворд, главы и уровни, задача дня, слово дня, карточки слов с русским переводом,
копилка бонусных слов, награды/задания/колесо. Код — форк `tatar-wow` («Сүз дөньясы»), данные и оформление — коми.

Запуск локально: открыть `index.html` в браузере (работает с `file://`) или
`cd /workspace/komi-wow && python3 -m http.server 8080` → http://localhost:8080/

Пересборка данных: `tools/fetch_sources.sh` (один раз) → `PYTHONHASHSEED=0 python3 tools/build_game.py 80 10` →
`python3 tools/verify_levels.py` (проверка уровней) → `python3 tools/scan_religion.py`. Всё сразу: `tools/rebuild_all.sh`.
Тесты (headless Chrome, `cd test && npm i`): `node dup_swipe.js`, `node test.js`, `node test_tutorial.js`.

Структура: `index.html`, `css/style.css`, `js/` (app.js — игра, art.js — процедурные SVG-пейзажи и коми-орнамент, i18n.js, platform.js +
adapters web/yandex/android, sound.js, ads-config.js с пустыми ID), `data/levels.js` + `data/cards/` (генерируются), `tools/`
(lexicon.py, build_game.py, religion_filter.py, verify_levels.py, kvwiki_freq.py, build_release.py …), `src/` (источники + ручные
правки переводов `ru_gloss_extra.json`, `ru_gloss_fix.json`), `test/`, `shots/`, `privacy/`, `release/*.md` (шаблоны чек-листов).
Ничего не опубликовано.
