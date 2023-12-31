# Распознаем речь
Данный проект позволяет запускать ботов для 2-х платформ: `VK` и `Telegram`.
Боты обучены на платформе `DialogFlow`.!

![Пример Telegram](https://github.com/serega19851/speech_recognition_bot/assets/110099338/82c69916-d8ce-4576-b52d-53185c4653af)

![Пример VK](https://github.com/serega19851/speech_recognition_bot/assets/110099338/a879e945-c6f3-46d0-b3ea-62840fa488c5)

## Что необходимо для запуска
Для данного проекта необходим `Python3.6` (или выше).
Создадим виртуальное окружение в корневой директории проекта:
```
python3 -m venv env
```
После активации виртуального окружения установим необходимые зависимости:
```
pip install -r requirements.txt
```
Также заранее создадим файл `.env` в директории проекта.

Теперь нам потребуется авторизоваться на `DialogFlow` для того, чтобы подключить к платформе ботов.

* Первое, что нужно сделать - это создать проект на `Google Cloud` по [ссылке](https://console.cloud.google.com/home/dashboard)
* Второе, авторизуемся на [DialogFlow](https://dialogflow.cloud.google.com/#/login) и создаём нового `агента`. **ВАЖНО!!!** Ваш `агент` должен быть привязан к проекту на `Google Cloud`.
* Третье, установим и настроим `Google Cloud CLI`, для того чтобы получить заветный `json-файл` с данными, которые необходимы для авторизации через `Python-код`. Для этого выполняем поочередно пункты по этой [ссылке](https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev).
После команды `gcloud auth application-default login` вам будет доступен путь к вашему `json-файлу`, запишите его в файл `.env` 
```
GOOGLE_APPLICATION_CREDENTIALS=
```
Также запишите ваш id проекта `Google Cloud`
```
PROJECT_ID=
```
## Создаём ботов
В проекте используются 2 телеграм бота, первый бот основной, второй - необходим для сбора логов. Подберите соответствующие названия для них.
Для создания телеграм ботов напишите [отцу ботов](https://telegram.me/BotFather).

Запишите их токены в `.env`:
```
TELEGRAM_TOKEN=
TELEGRAM_LOG=
```
Боту ошибок необходим ваш `телеграм id`, напишите [userinfobot](https://t.me/userinfobot) для его получения. Запишем его в `.env`:
```
TELEGRAM_CHAT_ID=
```
Для создания VK-бота для начала создадим группу, в которой уже потом запустим самого бота. В `управлении` созданной группы во вкладке `сообщения` убедимся, что сами сообщения включены, добавим их в левое меню и запишем преветствие.

Для получения `API токена` необходимо создать ключ во вкладке настроек `Работа с API`. Разрешим приложению `доступ к сообщениям сообщества`. Запишем токен в файл `.env`:
```
VK_GROUP_TOKEN=
```
## Тренируем DialogFlow

Пример запуска. По умолчанию путь до файла phrases_file.json ведет в папку проекта, но вы можете проложить свой путь до своего файла.
```
python dialog_learning.py
python dialog_learning.py -jp или --json_path ваш путь до файла

```

## Запуск ботов
Боты запускаются командами
```
python botspeech.py
python vk_bot.py 
```
При возникновении ошибок в любом из ботов, вы узнаете о них через бота журнала ошибок.
