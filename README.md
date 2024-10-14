# Менеджер Модов для Minecraft

Это приложение на Python с графическим интерфейсом, которое служит менеджером модов для игры Minecraft. Оно позволяет пользователю управлять модами, загружая их из интернета и сохраняя в указанную папку.

## 🛠️ Технологии и библиотеки

- **Язык программирования**: Python
- **Версия Python**: 3.8 или выше
- **Используемые библиотеки**:
  - `tkinter` - для создания графического интерфейса
  - `ttkthemes` - для применения тем оформления
  - `configparser` - для работы с конфигурационными файлами
  - `requests` - для выполнения HTTP-запросов

## 🌟 Инициализация и настройка интерфейса

- Используется библиотека `tkinter` для создания графического интерфейса.
- Приложение имеет тему "arc" благодаря использованию `ttkthemes`.
- Основное окно содержит элементы управления для выбора папки, добавления и удаления модов, а также для выбора версии Minecraft и загрузчика (loader).

## 🛠️ Работа с конфигурацией

- Используется `configparser` для чтения и записи настроек в файл `mods.ini`.
- Настройки включают папку для загрузки, версию Minecraft и тип загрузчика.

## 🗂️ Управление модами

- Пользователь может добавлять и удалять моды, вводя URL-адреса.
- Список модов сохраняется в конфигурационном файле и отображается в интерфейсе.

## ⬇️ Загрузка модов

- Приложение может загружать моды, проверяя их последнюю версию через API Modrinth.
- Если мод уже загружен и соответствует последней версии, он не будет загружен повторно.
- Старые версии модов удаляются перед загрузкой новых.

## 📝 Логирование

- Сообщения о действиях (успех или ошибка) выводятся в текстовую консоль в интерфейсе.

## 👤 Интерфейс пользователя

- Включает кнопки для выбора папки, добавления и удаления модов, обновления списка модов и загрузки модов.
- Поля ввода для URL модов, версии Minecraft и типа загрузчика.

## 🚀 Сборка и запуск проекта

1. Убедитесь, что у вас установлена версия Python 3.8 или выше.
2. Установите необходимые библиотеки, выполнив команду:
   ```bash
   pip install -r requirements.txt
   ```
3. Запустите приложение с помощью следующей команды:
   ```bash
   python minefix.py
   ```

Приложение позволяет пользователю легко управлять модами для Minecraft, обеспечивая удобный интерфейс для выполнения всех необходимых действий.