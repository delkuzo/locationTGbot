# Location TG Bot 📍

Telegram бот, который предоставляет интересные факты о любом месте на основе геолокации, используя GPT-4o-mini.

## 🚀 Возможности

- **Факты о местах**: Отправьте геолокацию и получите уникальный факт о месте в радиусе 500 метров
- **Rate limiting**: Защита от спама (1 запрос в 5 секунд на пользователя)
- **Поддержка команд**: `/start` и `/help` для навигации
- **Webhook интеграция**: Работает через FastAPI webhook для надежной доставки сообщений

## 📋 Требования

- Python 3.12+
- Telegram Bot Token (получить у [@BotFather](https://t.me/botfather))
- OpenAI API Key (получить на [platform.openai.com](https://platform.openai.com))

## 🛠 Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/location-tg-bot.git
cd location-tg-bot
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Скопируйте `.env.example` в `.env` и заполните значения:

```bash
cp .env.example .env
```

Отредактируйте `.env`:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
WEBHOOK_URL=https://your-domain.com  # Для production
```

## 🏃‍♂️ Запуск

### Локальный запуск

```bash
python -m uvicorn bot.main:app --reload
```

Бот будет доступен на `http://localhost:8000`

### Запуск через Docker

```bash
docker build -t location-tg-bot .
docker run -p 8000:8000 --env-file .env location-tg-bot
```

## 🧪 Тестирование

### Запуск тестов

```bash
pytest
```

### Запуск с покрытием

```bash
pytest --cov=bot --cov-report=html
```

### Проверка кода

```bash
# Линтинг
ruff check .

# Форматирование
black .
```

## 📦 Деплой на Railway

1. Создайте проект на [Railway](https://railway.app)

2. Подключите GitHub репозиторий

3. Добавьте переменные окружения в Railway:
   - `TELEGRAM_BOT_TOKEN`
   - `OPENAI_API_KEY`
   - `WEBHOOK_URL` (будет предоставлен Railway)

4. Railway автоматически задеплоит приложение при push в main ветку

## 🔧 Конфигурация Webhook

После деплоя бот автоматически установит webhook. Для ручной установки:

```bash
curl -X POST https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook \
  -H "Content-Type: application/json" \
  -d '{"url": "https://your-domain.com/webhook"}'
```

## 📁 Структура проекта

```
locationTGbot/
├── bot/
│   ├── __init__.py
│   ├── main.py              # FastAPI приложение
│   ├── handlers/            # Обработчики команд
│   │   ├── __init__.py
│   │   └── location.py
│   └── services/            # Внешние сервисы
│       ├── __init__.py
│       ├── openai_client.py
│       └── rate_limiter.py
├── config/
│   ├── __init__.py
│   └── settings.py          # Настройки приложения
├── tests/                   # Тесты
├── .env.example            # Пример переменных окружения
├── requirements.txt        # Зависимости
├── Dockerfile             # Docker образ
├── railway.json          # Конфигурация Railway
└── README.md            # Этот файл
```

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature ветку (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📝 Лицензия

Этот проект лицензирован под MIT License.

## 🆘 Поддержка

Если у вас возникли проблемы, создайте [Issue](https://github.com/yourusername/location-tg-bot/issues) в репозитории. 