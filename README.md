# LMS - Django приложение с Docker

Этот репозиторий содержит Django приложение, настроенное для работы с Docker и Docker Compose. Настройка включает в себя веб-приложение Django, базу данных PostgreSQL, Redis и Celery для фоновых задач.

## Предварительные требования

Перед началом работы убедитесь, что на вашей системе установлены:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Настройка окружения

1. Клонируйте этот репозиторий:
   ```bash
   git clone https://github.com/VladimirSulym/hw_modul_8
   cd hw_modul_8
   ```

2. Создайте файл `.env` в корне проекта со следующими переменными (при необходимости измените значения):
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True

   CSU_PASS=your-custom-user-password

   # Конфигурация базы данных
   DATABASE_NAME=hw_modul_8
   DATABASE_USER=postgres
   DATABASE_PASSWORD=your-db-password
   DATABASE_HOST=db
   DATABASE_PORT=5432

   # Конфигурация электронной почты
   EMAIL_HOST=smtp.your-email-provider.com
   EMAIL_HOST_USER=your-email@example.com
   EMAIL_HOST_PASSWORD=your-email-password
   EMAIL_PORT=465
   EMAIL_USE_SSL=True

   # Ключ API Stripe (если используется функциональность платежей)
   STRIPE_API_KEY=your-stripe-api-key
   ```

   Примечание: Убедитесь, что установлено `DATABASE_HOST=db` для среды Docker.

## Сборка и запуск с Docker

1. Соберите и запустите все сервисы:
   ```bash
   docker-compose up -d
   ```

   Эта команда:
   - Создаст Docker образы, если они не существуют
   - Запустит все сервисы, определенные в docker-compose.yml
   - Выполнит миграции базы данных
   - Загрузит начальные данные
   - Запустит сервер разработки Django

2. Для просмотра логов всех контейнеров:
   ```bash
   docker-compose logs -f
   ```

3. Для просмотра логов определенного сервиса:
   ```bash
   docker-compose logs -f web
   ```

## Доступ к приложению

После запуска контейнеров:
- Веб-приложение: http://localhost:8000
- База данных: PostgreSQL работает на порту 5432 (внутри сети Docker)
- Redis: Работает на порту 6379 (внутри сети Docker)
- В рамках команды "python manage.py lid" создан суперпользователь admin@admin.ru с паролем из файла .env (CSU_PASS)

## Дополнительные команды

### Выполнение команд управления Django

```bash
docker-compose exec web python manage.py <command>
```

### Остановка сервисов

```bash
docker-compose down
```

### Остановка и удаление томов

```bash
docker-compose down -v
```

### Пересборка сервисов

```bash
docker-compose up -d --build
```

## Устранение неполадок

1. Если веб-сервис не запускается, проверьте, работает ли база данных:
   ```bash
   docker-compose ps
   ```

2. Если вам нужно сбросить базу данных:
   ```bash
   docker-compose down -v
   docker-compose up -d
   ```

3. Для проверки логов на наличие ошибок:
   ```bash
   docker-compose logs -f
   ```

4. Если вы вносите изменения в Dockerfile или requirements.txt, пересоберите образы:
   ```bash
   docker-compose build
   docker-compose up -d
   ```
