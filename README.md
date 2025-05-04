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

## Настройка удаленного сервера и деплой

### Требования к серверу

- Ubuntu 20.04 LTS или новее
- Минимум 2 ГБ оперативной памяти
- Минимум 20 ГБ дискового пространства
- Открытые порты: 22 (SSH), 80 (HTTP), 443 (HTTPS)

### Подготовка сервера

1. Обновите пакеты на сервере:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. Установите Docker:
   ```bash
   sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
   sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
   sudo apt update
   sudo apt install -y docker-ce
   sudo systemctl enable docker
   sudo systemctl start docker
   sudo usermod -aG docker $USER
   ```

3. Установите Docker Compose:
   ```bash
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.6/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

4. Создайте директорию для проекта:
   ```bash
   mkdir -p ~/django/hw_modul_8
   ```

### Настройка SSH ключей

1. На локальной машине сгенерируйте SSH ключ (если у вас его еще нет):
   ```bash
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   ```

2. Скопируйте публичный ключ на сервер:
   ```bash
   ssh-copy-id username@server_ip
   ```

3. Проверьте подключение:
   ```bash
   ssh username@server_ip
   ```

### Настройка GitHub Actions

1. В репозитории GitHub перейдите в Settings -> Secrets and variables -> Actions
2. Добавьте следующие секреты:
   - `DATABASE_NAME`: имя базы данных
   - `DATABASE_USER`: имя пользователя базы данных
   - `DATABASE_PASSWORD`: пароль пользователя базы данных
   - `SECRET_KEY`: секретный ключ Django
   - `DEBUG`: значение для настройки DEBUG (True или False)
   - `DOCKER_HUB_USERNAME`: имя пользователя Docker Hub
   - `DOCKER_HUB_ACCESS_TOKEN`: токен доступа Docker Hub
   - `SERVER_HOST`: IP-адрес вашего сервера
   - `SERVER_USERNAME`: имя пользователя на сервере
   - `SSH_PRIVATE_KEY`: содержимое приватного SSH ключа (cat ~/.ssh/id_rsa)
   - `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_SSL`: настройки для отправки электронной почты

### Ручной деплой на сервер

Если вы хотите выполнить деплой вручную без использования GitHub Actions:

1. Клонируйте репозиторий на сервер:
   ```bash
   cd ~/django/hw_modul_8
   git clone https://github.com/VladimirSulym/hw_modul_8 .
   ```

2. Создайте файл .env с необходимыми переменными окружения:
   ```bash
   nano .env
   ```

   Содержимое файла .env:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=False

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
   ```

3. Запустите приложение с помощью Docker Compose:
   ```bash
   docker-compose up -d
   ```

### Автоматический деплой через GitHub Actions

При настроенном GitHub Actions деплой будет происходить автоматически при каждом push в репозиторий:

1. Workflow выполнит проверку кода с помощью Flake8
2. Запустит тесты
3. Соберет Docker образы и отправит их в Docker Hub
4. Подключится к серверу по SSH
5. Обновит код из репозитория
6. Загрузит последние версии Docker образов
7. Перезапустит сервисы с помощью Docker Compose

### Проверка работоспособности

После деплоя проверьте, что приложение работает:

1. Откройте в браузере http://your_server_ip
2. Проверьте логи контейнеров:
   ```bash
   docker-compose logs -f
   ```

### Обновление приложения

Для обновления приложения достаточно отправить изменения в репозиторий GitHub, и GitHub Actions автоматически выполнит деплой.

### Устранение неполадок на сервере

1. Проверьте статус контейнеров:
   ```bash
   docker-compose ps
   ```

2. Проверьте логи:
   ```bash
   docker-compose logs -f
   ```

3. Перезапустите контейнеры:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

4. Проверьте использование дискового пространства:
   ```bash
   df -h
   ```

5. Очистите неиспользуемые Docker ресурсы:
   ```bash
   docker system prune -f
   ```
