# HTTP Endpoint Monitor

Небольшой сервис на **FastAPI** для мониторинга списка URL-эндпоинтов, подсчёта успешных ответов (только 2xx) и выдачи статистики через REST API.

---

## 🚀 Инструкция по запуску

1. Клонируйте репозиторий и перейдите в корень проекта:

   ```bash
   git clone https://github.com/Huen1x/HTTP-Endpoint-Monitor.git
   cd http-endpoint-monitor
   ```

2. Установите зависимости:

   ```bash
   pip install -r src/requirements.txt
   ```

3. (Опционально) Соберите и запустите контейнер Docker:

   ```bash
   # из корня проекта
   docker build -t endpoint-monitor .
   docker run -d -p 8000:8000 endpoint-monitor
   ```

4. Запустите приложение локально (без Docker):

   ```bash
   cd src
   uvicorn main:app --reload
   ```

5. Чтобы убедиться, что всё запущено корректно, откройте в браузере один из следующих адресов:

   * **API**: `http://127.0.0.1:8000`
   * **Swagger UI**: `http://127.0.0.1:8000/docs`

---

## 🔌 Описание API

Все маршруты доступны под префиксом `/endpoints`.

### Добавить URL

* **POST** `/endpoints/`
* **Body** (JSON):

  ```json
  { "url": "https://example.com" }
  ```
* **Успех**: `201 Created`

  ```json
  { "id": 1, "url": "https://example.com", "count": 0 }
  ```

### Проверить URL

* **POST** `/endpoints/{id}/check`
* **Успех**: `200 OK`

  ```json
  { "status": 200, "counted": true }
  ```

### Получить список

* **GET** `/endpoints/?sort=asc|desc`
* **Query-параметр**:

  * `sort` — `asc` или `desc` (по умолчанию `desc`)
* **Успех**: `200 OK`

  ```json
  [
    { "id": 1, "url": "...", "count": 5 },
    { "id": 2, "url": "...", "count": 3 }
  ]
  ```

### Удалить URL

* **DELETE** `/endpoints/{id}`
* **Успех**: `204 No Content`

---

## 🧪 Тестирование

Проект покрыт тестами с использованием **pytest**.

* **tests/test/test_logic.py** — unit-тесты для логики инкремента счётчика
* **tests/test/test_api.py** — интеграционные тесты для REST API с SQLite

### Запуск тестов

```bash
pytest
```
