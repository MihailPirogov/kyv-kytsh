# Кыв кытш — ответы для форм Google Play Console (и коротко для RuStore / Яндекс Игр)

Приложение `ru.pirogovlab.kyvkytsh`, версия 1.0.0 (versionCode 1), файл `release/kyv-kytsh.aab` (подпись — собственный ключ Кыв кытш, SHA-256 `5B:A3:62:F3:1F:3F:7D:8C:38:68:70:E4:82:B5:36:CD:8F:C3:F9:6D:79:17:10:85:BB:2C:20:87:63:69:18:1C`; в Play это будет ключ загрузки, Play App Signing).
Политика конфиденциальности: **https://pirogovlab.ru/kyv-kytsh/privacy/** (редакция с рекламой).

Что приложение реально отправляет с устройства:
1. **Yandex Mobile Ads SDK 8.6.0** (баннер ID ещё не создан (сейчас demo-*-yandex), межстраничная ID ещё не создан (сейчас demo-*-yandex), за вознаграждение ID ещё не создан (сейчас demo-*-yandex)): рекламный идентификатор (разрешение `com.google.android.gms.permission.AD_ID` в манифесте) и технические данные для показа рекламы. Местоположение не отправляет (locationConsent не включён, разрешений на геолокацию нет).
2. Больше ничего: нет сервера разработчика, таблиц лидеров, аккаунтов, аналитики разработчика, Firebase и покупок. Прогресс хранится только на устройстве. Нет доступа к контактам, файлам, камере, микрофону, геолокации.

(Шаблон — формы «Марий мут», ru.pirogovlab.mariwordle, опубликованного в том же аккаунте; отличие — у Кыв кытш нет таблицы лидеров и ника.)

## 1. Privacy policy
`https://pirogovlab.ru/kyv-kytsh/privacy/`

## 2. Ads
**Contains ads: Yes.**

## 3. App access
**All functionality is available without special access.**

## 4. Advertising ID
Uses advertising ID: **Yes** → purpose **Advertising or marketing** (Yandex Mobile Ads SDK).

## 5. Target audience and content
- Age groups: **13–15, 16–17, 18 and over** (не отмечать младше 13: Yandex Mobile Ads не входит в список SDK программы Families). Содержание при этом 0+.
- «Could your store listing unintentionally appeal to children?» → **No** (словесная головоломка для изучающих язык, без мультперсонажей).

## 6. Data safety
| Вопрос | Ответ |
|---|---|
| Does your app collect or share any of the required user data types? | **Yes** |
| Is all of the user data collected by your app encrypted in transit? | **Yes** (TLS в Yandex Mobile Ads SDK) |
| Account creation | **My app does not allow users to create an account** |
| Do you provide a way for users to request that their data be deleted? | **No** — разработчик ничего не хранит; рекламный ID пользователь сбрасывает/удаляет в настройках Android; прогресс удаляется вместе с приложением |

Типы данных — отметить **только один**:
| Категория → тип | Collected | Shared | Ephemeral | Required/Optional | Цели |
|---|---|---|---|---|---|
| Device or other IDs → **Device or other IDs** (рекламный ID для Yandex Mobile Ads) | Yes | **Yes** (Яндекс, рекламная сеть) | No | **Optional** (ID можно сбросить/удалить, отключить персонализацию) | Collection: **Advertising or marketing**; Sharing: **Advertising or marketing** |

Не отмечать: Location, Personal info, Financial, Health, Messages, Photos/Videos, Audio, Files, Calendar, Contacts, App activity, Web browsing, App info and performance.
Основание: официальная таблица Яндекса «Data safety in Google Play» для Mobile Ads SDK 8 (ads.yandex.com/helpcenter/en/dev/android/app-privacy-android) — так же заполнено у «Марий мут». Перед отправкой открыть ссылку и сверить, не поменялась ли таблица.

## 7. Content rating (IARC)
Email mihail.pirogov@gmail.com · Category **Game** (Puzzle/Word).
| Вопрос | Ответ |
|---|---|
| Violence / Fear / Sexuality / Nudity | **No** |
| Language: profanity, crude humour | **No** (ненормативная лексика исключена из словаря) |
| Controlled substances | **No** |
| Gambling, simulated gambling, loot boxes | **No** — «колесо удачи» — бесплатное ежедневное вращение за игровые монеты, без ставок и покупок |
| Crude / discriminatory content | **No** |
| Users interact or exchange content | **No** (нет чата, ников, таблиц) |
| Shares user's location | **No** |
| Purchases of digital goods | **No** |
| Web browser / unrestricted internet | **No** |
| Ads (если спросит) | **Yes** |
Ожидаемо: **PEGI 3 / ESRB Everyone / USK 0 / IARC 3+**.

## 8. Прочие декларации
News: No · Government: No · Financial features: None · Health: None · COVID-19: No · Foreground service / full-screen intent / exact alarms: не используются · Data deletion for accounts: не применимо.

## 9. Store settings
App or game: **Game** · Category: **Word** · Tags: Word, Puzzle, Crossword, Casual, Offline · email mihail.pirogov@gmail.com · website **https://pirogovlab.ru** (нужен для app-ads.txt: `yandex.com, 1969132, DIRECT` уже есть) · Free · страны: все (или Россия + остальные по желанию).

## RuStore — те же ответы коротко
Тип **Игра** · категории: основная **Словесные игры**, доп. **Головоломки** · возраст **0+** · реклама **есть** (Рекламная сеть Яндекса) · платного контента нет · политика https://pirogovlab.ru/kyv-kytsh/privacy/ · файл `release/kyv-kytsh.apk` (тот же ключ Кыв кытш).

## Яндекс Игры
Возраст 0+. Рекламу и данные показывает платформа; ссылок в игре нет (сборка вырезает домены и внешние ссылки).
