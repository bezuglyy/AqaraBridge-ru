# Changelog

## 2.1.2-ru3

- добавлена поддержка виртуального IR-телевизора M3 (`virtual.ir_local.tv`);
- новый класс `AiotIRTVEntity` в `remote.py`: загрузка кнопок пульта (`query.ir.keys`), отправка команд (`write.ir.click`);
- в `aiot_cloud.py` добавлен метод `async_query_ir_keys`;
- добавлен маппинг ресурса `virtual.ir_local.tv` (remote);
- исправлен `_LOGGER` в `remote.py` (добавлен импорт logging).

## 2.1.2-ru2

- добавлена поддержка виртуального IR-кондиционера M3 (`virtual.ir_local.ac`);
- новый класс `AiotIRACEntity` в `climate.py`: режимы cool/heat/auto/dry/fan_only, вентилятор auto/low/medium/high, качание off/on, температура 16–30°C, шаг 1°C;
- добавлены методы облака: `async_query_ir_acstate`, `async_write_ir_click`, `async_write_ir_startlearn`, `async_write_ir_cancellearn`, `async_query_ir_learnresult`;
- добавлен маппинг ресурса `virtual.ir_local.ac` с параметрами климата;
- переработан `core/aiot_cloud.py` (рефакторинг, корректное обновление токена).

## 2.1.2-ru1

- исправлено обновление токена с корректным `await`;
- исправлен вызов `gen_auth_entry(...)`;
- исправлена загрузка платформ через `async_forward_entry_setups(...)`;
- добавлена корректная выгрузка платформ в `async_unload_entry`;
- исправлены части `config_flow` и `options flow`;
- добавлен русский перевод интерфейса;
- обновлены README, HACS-описание и метаданные репозитория;
- добавлены логотип и иконка проекта.
