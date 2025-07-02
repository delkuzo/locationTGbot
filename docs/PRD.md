### Product Requirements Document

## 1. Overview / Problem

Создать Telegram-бота-MVP, который по одной команде — получив точку на карте — возвращает пользователю необычный факт о любом месте рядом с этой точкой, запрашивая GPT-4.1-mini. Проект нужен как быстрый одновечерний прототип, который затем можно расширить живой локацией.

## 2. Key User Flows

1. **Share location** → Бот принимает геометку → Запрашивает OpenAI → Отправляет факт.
2. **(v1.1) Share live location** → Бот подписывается на обновления точки → Каждые 10 минут присылает новый факт → Отправки прекращаются по истечении live-period либо по команде stop.

## 3. Functional Requirements

* **Приём геометки.** Бот читает `update.message.location`, объект `Location` c полями
  `latitude`, `longitude`, `horizontal_accuracy?`, `live_period?`, `heading?`, `proximity_alert_radius?` ([core.telegram.org][1], [core.telegram.org][1])
  Live-location приходит как `edited_message` с теми же полями; обновления продолжаются в пределах `live_period` ([core.telegram.org][2])
* **Запрос к OpenAI.**
  `POST https://api.openai.com/v1/chat/completions`

  * model: `gpt-4o-mini`
  * system prompt: «Ты гид по местности…»
  * user content: JSON `{lat, lon}`
  * temperature ≈ 1, max\_tokens ≈ 200.
* **Формирование ответа.** Возвращать 1–2 предложения, ≤ 512 символов, без Markdown-ссылок.
* **Обработка ошибок.** Таймаут GPT ⇒ ответ «Не смог найти факт, пришли точку ещё раз».
* **Ограничения.**

  * ≤ 1 запроса в 5 сек. на пользователя;
  * логирование только технических метрик, без хранения координат.
* **(v1.1) Таймер.** При живой локации запускать cron-loop 10 мин.; при stop/истечении live\_period останавливать.

## 4. Non-Goals

* Поддержка команд кроме location / stop.
* Хранение истории запросов.
* Рекомендации маршрутов, ресторанов, платных API карт.

## 5. Milestones & Release Plan

| Дата                    | Цель                 | Задачи                                                                      |
| ----------------------- | -------------------- | --------------------------------------------------------------------------- |
| **Tonight (v1.0)**      | MVP location-to-fact | init repo; parse `/location`; обвязка OpenAI; deploy on Railway; smoke-test |
| +1 ч                    | Polish               | rate-limits; i18n RU/EN; README                                             |
| **v1.1 (next evening)** | Live-location facts  | webhook edits; 10-min scheduler; `/stop`                                    |
| **v1.2 (later)**        | Nice-to-haves        | caching facts, unit-tests, CI, Docker, infra-monitoring                     |
