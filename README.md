# Aqara Bridge

Кастомная интеграция для [Home Assistant](https://www.home-assistant.io) · версия **2.1.2-ru3**.

![icon](custom_components/aqara_bridge/brand/icon.png)

| | |
|---|---|
| Домен | `aqara_bridge` |
| Версия | 2.1.2-ru3 |
| Тип | custom integration |

## Описание

Интеграция хаба Aqara (M1S/M2/M3 и др.) — русская локализация.

## Возможности

- Датчики качества воздуха
- Бинарные датчики (движение, контакты и т.п.)
- Управление климатом
- Управление шторами/жалюзи
- События
- Управление светом
- Удалённое управление (ИК и т.п.)
- Сенсоры и мониторинг состояния
- Переключатели и вкл/выкл устройства

## Установка

1. Скопируйте папку `custom_components/{domain}/` в каталог `custom_components/` конфигурации Home Assistant.
2. Перезапустите Home Assistant.
3. Настройки → Устройства и службы → Добавить интеграцию → **{mname}**.

> Установка через HACS: добавьте репозиторий `https://github.com/bezuglyy/{repo}` как Custom repository (категория Integration).

## Лицензия

MIT
