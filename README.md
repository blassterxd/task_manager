# Менеджер задач (task_manager)

Веб-приложение на Django 5.2: регистрация, вход и управление личными задачами
(название, описание, срок, приоритет, состояние). Оформление: django-bootstrap4.

## Возможности

- регистрация, вход и выход (выход только методом POST);
- создание, редактирование, удаление (с подтверждением) задач;
- переключение «выполнена» / «в работе»;
- пользователь видит только свои задачи, чужие id дают 404.

## Порядок списка задач

1. невыполненные раньше выполненных;
2. высокий приоритет, затем обычный, затем низкий;
3. ближайший срок выполнения;
4. задачи без срока в конце.

## Локальный запуск (Python 3.12)

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows:     .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Тесты: `python manage.py test`

## Развёртывание на сервере (Docker Compose)

1. Подключитесь к серверу и создайте каталог проекта:
   `ssh student@192.168.1.11`, затем `newproject ФАМИЛИЯ-task-manager`.
   Команда создаст каталог и файл `.env` с портами (`PORT1`).
2. Загрузите код:
   ```bash
   cd ~/projects/ФАМИЛИЯ-task-manager
   git init -q
   git remote add origin https://github.com/ЛОГИН/task_manager.git
   git pull origin HEAD
   ```
3. Допишите в `.env` переменные из таблицы ниже (образец в `.env.example`).
4. Запустите: `docker compose up -d --build`, проверьте: `docker compose ps`
   (статус `Up (healthy)`).
5. Создайте администратора:
   `docker compose exec web python manage.py createsuperuser`.
6. Откройте `http://192.168.1.11:PORT1/`.

Обновление: `git pull origin HEAD`, затем `docker compose up -d --build`.

## Переменные окружения (файл `.env`, в репозиторий не входит)

| Переменная | Назначение | Пример |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | секретный ключ Django | длинная случайная строка |
| `DJANGO_DEBUG` | режим отладки | `False` |
| `DJANGO_ALLOWED_HOSTS` | допустимые адреса через запятую | `192.168.1.11,localhost,127.0.0.1` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | адрес сайта с портом | `http://192.168.1.11:20010` |
| `DJANGO_USE_HTTPS` | включить защищённые cookie (при HTTPS) | `False` |
| `SQLITE_PATH` | путь к базе внутри контейнера | `/app/data/db.sqlite3` |
| `PORT1` | внешний порт (выдаёт `newproject`) | `20010` |

База данных хранится в томе Docker и не теряется при пересборке.