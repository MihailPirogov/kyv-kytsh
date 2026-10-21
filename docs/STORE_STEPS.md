# Кыв кытш 1.0.0 — план публикации (ничего не отправлено)

| | |
|---|---|
| Название | **Кыв кытш** (запасное: «Кыв кытш — коми слова») |
| Пакет | `ru.pirogovlab.kyvkytsh` · 1.0.0 (versionCode 1) · minSdk 24 · targetSdk 36 |
| Реклама | Yandex Mobile Ads, приложение РСЯ **20259432** (R-M-20259432-1 баннер, -2 межстраничный, -3 с вознаграждением) |
| Подпись | собственный ключ Кыв кытш (см. ANDROID_CHECKLIST.md) |
| Политика | https://pirogovlab.ru/kyv-kytsh/privacy/ (выложить версию с рекламой как постоянную) |
| Страница игры | https://pirogovlab.ru/kyv-kytsh-igra/ (подготовлена в site_stage/out, не опубликована) |
| Тексты / формы | `release/store/TEXTS_ru.md`, `TEXTS_en.md`, `PLAY_FORMS.md` |

Порядок:
0. **РСЯ (partner.yandex.ru)**: создать приложение + 3 блока → вписать в `android/app/src/main/res/values/ads.xml` → `tools/build_android.sh`.
1. **Сайт**: выложить privacy (постоянную), APK в /kyv-kytsh/, лендинг/блог из `site_stage/out/` (после одобрения Михаила). Игра /kyv-kytsh/ остаётся noindex и вне sitemap.
2. **RuStore** (console.rustore.ru): Игра «Кыв кытш», APK `kyv-kytsh-rustore.apk`, тексты TEXTS_ru.md, графика `rustore_assets/`, 0+, реклама — да.
3. **Google Play Console**: новое приложение «Кыв кытш», ru-RU, игра, бесплатно; анкеты по PLAY_FORMS.md; графика `play_assets/`; Production (как у других игр аккаунта) или закрытый тест, если консоль потребует; Play App Signing; `kyv-kytsh.aab`.
4. **Яндекс Игры** (games.yandex.ru/console): по `YANDEX_CHECKLIST.md`, архив `kyv-kytsh-yandex.zip`, ассеты `yandex_assets/`.
5. **РСЯ**: добавить ссылку на магазин в приложение → модерация.
6. **После публикации**: ссылки магазинов на лендинге (PLACEHOLDER stores, убрать hidden) и в README GitHub; `git push` в MihailPirogov/kyv-kytsh (репозиторий на GitHub создать вручную).
