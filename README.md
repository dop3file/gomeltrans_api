# gomeltrans_api
**JSON API** для получения информации о **гомельском общественном транспорте**

*Источник - https://gomeltrans.net/*

# Как устроено API

**API** асинхронно c помощью **BeautifulSoup + aiohttp** парсит информацию о транспорте с сайта https://gomeltrans.net/, сериализуют и сохраняет в **JSON** файл

Для того, чтобы не нагружать источник, но и сохранять актуальную информацию, повторный парсинг происходит каждые сутки в фоновом режиме с помощью **Django Q**

# Методы API

Первый аргумент - тип транспорта(на данный момент bus и trolleybus)

number - номер транспорта

**route/\<str:type_transport\>/\<str:number\>** - получение информации(откуда,куда,остановки) о конкретном маршруте

Пример возвращаемого значения:
```
{
    "response" : {
        "1": {
            "from": "Вокзал",
            "to": "Микрорайон «Любенский»",
            "mode": "ежедневно",
            "tariff_price": "80к./85к.",
            "route_length": 14.09,
            "count_stops": 26,
            "similar_routes": [
                "34"
            ],
            "stops": {
              "to": {
                    "Вокзал": {
                        "week": [
                            "6:03",
                            "6:54",
                            ...
                        ],
                        "weekend": [
                          "6:09",
                          "6:34",
                          ...
                        ]
                    }
                "back": {
                    "Микрорайон «Любенский»": {
                        "week": [
                            "6:03",
                            "6:54",
                            ...
                        ],
                        "weekend": [
                          "6:09",
                          "6:34",
                          ...
                        ]
                    }
           }
     },
     "status_code": 200
}
```

**route/\<str:type_transport\>/name_all** - получения номеров всех маршрутов 

# Requirements
 - **BeautifulSoup4**
 - **asyncio**
 - **aiohhtp**
 - **django**
 - **django-q**

# Попробовать - https://gomeltrans.pythonanywhere.com/bus/route/1/



