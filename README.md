# FastAPI RabbitMQ Service

## Описание
Служба FastAPI для генерации UUID, обработки заголовков и интеграции с RabbitMQ для обработки сообщений.

## Настройка

### Требования
- Docker
- Docker Compose

### Запуск приложения
1. Произведите клонирование репозиторий:
    ```bash
    git clone https://github.com/HAXF13D/other_code_test
    ```
2. Перейдите в папку с проектом:
    ```bash
    cd other_code_test
    ```
3. Соберите и запустите приложение с помощью Docker Compose:
    ```bash
    docker-compose up --build
    ```
4. Зайдите в службу FastAPI по адресу `http://localhost:8000`.

### Конечные точки API
- `GET /generate-uuid`: Генерирует случайный UUID. Может принимать заголовок `X-Flag` (`зеленый` или `красный`).
