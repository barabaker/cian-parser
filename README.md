# Парсер данных с сайта CIAN

Этот проект представляет собой парсер данных с сайта [CIAN](https://www.cian.ru/), который использует API для получения информации о предложениях недвижимости. Данные сохраняются в MongoDB, а также загружаются фотографии и создаются скриншоты страниц.

## Как это работает

### Получение данных с API

Проект использует фреймворк [Crawlee](https://crawlee.dev/) для работы с API CIAN. Основная логика заключается в формировании `payload` и отправке запроса к эндпоинту:

```python
def make_payload(self):
    payload = {
        "jsonQuery": {
            "_type": f"{self.offer_type}sale",
            "engine_version": {"type": "term", "value": 2},
            'region': {
                'type': 'terms',
                'value': self.subject_id,
            },
            "bbox": {
                "type": "term",
                "value": self.bbox
            },
            "page": {"type": "term", "value": self.page},
        }
    }
    return payload
```
#### Запрос отправляется на эндпоинт:
```python
url = 'https://api.cian.ru/search-engine/v1/search-offers-mobile-site/'
```

## Обработка ответа
В ответе от API нас интересуют два ключа:

 - data.get("offersCount", 0) — количество предложений.
 - data.get('offers', []) — список предложений.

## Логика обработки данных:
- Если offersCount > 420, то область поиска (bbox) делится на более мелкие части, чтобы уменьшить количество предложений в каждой области.
- Если offersCount < 420, то применяется пагинация для получения всех предложений.

## Загрузка фотографий
В отдельном контейнере запускается воркер, который загружает фотографии в формате base64 в отдельную коллекцию MongoDB. Воркер ориентируется на поле updated_at, чтобы загружать только новые или обновленные фотографии.

## Создание скриншотов
Еще один воркер отвечает за рендеринг страниц и создание скриншотов. Он также ориентируется на поле updated_at, чтобы обрабатывать только новые или обновленные предложения.


---

## Архитектура системы

Ниже представлена схема взаимодействия компонентов системы:

```mermaid
graph TD
    A[MongoDB] -->|1. Чтение документов| B[Producer]
    B -->|2. Отправка задач| C[RabbitMQ]
    C -->|3. Получение задач| D[Consumer]
    D -->|4. Сохранение результатов| A
    B -->|5. Обновление состояния| A
```