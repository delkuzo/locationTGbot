# Заметки по деплою Location TG Bot

## Текущий статус
- ✅ Код бота написан и протестирован локально
- ✅ Репозиторий создан на GitHub
- ❌ Деплой на Railway не удался

## Проблемы при деплое на Railway

1. **Docker timeout** - сборка образа занимает слишком много времени
2. **Nixpacks конфликты** - Railway игнорирует конфигурационные файлы
3. **Неправильный webhook URL** - установлен GitHub URL вместо Railway URL

## Что нужно сделать при возврате к проекту

### Шаг 1: Настройка переменных окружения в Railway
```
TELEGRAM_BOT_TOKEN=ваш_токен_от_@BotFather
OPENAI_API_KEY=ваш_ключ_от_OpenAI
WEBHOOK_URL=https://ваш-railway-url.railway.app
```

### Шаг 2: Альтернативные платформы для деплоя
Если Railway не работает, попробовать:
- **Render.com** (бесплатный план)
- **Heroku** (платный)
- **DigitalOcean App Platform**
- **Vercel** (для FastAPI проектов)

### Шаг 3: Локальное тестирование
```bash
# Установка зависимостей
pip install -r requirements.txt

# Создание .env файла
cp .env.example .env
# Заполнить токены в .env

# Запуск локально
python -m uvicorn bot.main:app --reload

# Тестирование бота
python test_bot.py
```

### Шаг 4: Ручная настройка webhook
```bash
curl -X POST https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook \
  -H "Content-Type: application/json" \
  -d '{"url": "https://your-app-url.com/webhook"}'
```

## Полезные endpoint'ы для диагностики
- `/` - статус приложения
- `/health` - проверка здоровья
- `/config` - проверка конфигурации (токены установлены?)
- `/webhook/info` - информация о webhook
- `/webhook/set` - ручная установка webhook

## Файлы проекта

### Конфигурационные файлы для деплоя:
- `Procfile` - для Heroku/Render
- `railway.toml` - для Railway
- `Dockerfile` - для Docker деплоя
- `requirements.txt` - зависимости Python

### Основной код:
- `bot/main.py` - FastAPI приложение
- `bot/handlers/location.py` - обработчики Telegram
- `bot/services/openai_client.py` - клиент OpenAI
- `config/settings.py` - настройки проекта

## Рабочие варианты конфигурации

### Для Render.com:
```yaml
# render.yaml
services:
  - type: web
    name: location-tg-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python -m uvicorn bot.main:app --host 0.0.0.0 --port $PORT
```

### Для Heroku:
- Использовать `Procfile` (уже создан)
- Установить buildpack: `heroku/python` 