#!/bin/bash
# Download the open sources into src/ (licences: SOURCES.md)
set -e
cd "$(dirname "$0")/../src"
B="https://kaikki.org/ruwiktionary/%D0%9A%D0%BE%D0%BC%D0%B8-%D0%B7%D1%8B%D1%80%D1%8F%D0%BD%D1%81%D0%BA%D0%B8%D0%B9"
curl -fsS -o ru_kv.jsonl "$B/kaikki.org-dictionary-%D0%9A%D0%BE%D0%BC%D0%B8%D0%B7%D1%8B%D1%80%D1%8F%D0%BD%D1%81%D0%BA%D0%B8%D0%B9.jsonl"
curl -fsS -o en_kv.jsonl "https://kaikki.org/dictionary/Komi-Zyrian/kaikki.org-dictionary-KomiZyrian.jsonl"
curl -fsS -o kvwiki.xml.bz2 "https://dumps.wikimedia.org/kvwiki/latest/kvwiki-latest-pages-articles.xml.bz2"
python3 ../tools/kvwiki_freq.py
git clone -q --depth 1 https://github.com/giellalt/dict-kpv-rus.git || (cd dict-kpv-rus && git pull -q)
