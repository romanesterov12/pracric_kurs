# FitTracker - Персональная система фитнес-трекинга

Полнофункциональная веб-платформа для отслеживания питания, физической активности и получения персонализированных рекомендаций.

## Возможности

### Для пользователей:
- Регистрация и детальный профиль с антропометрическими данными
- Трекинг питания с поиском по БЖУ
- Трекинг физической активности
- Ежедневный мониторинг показателей (вес, сон, настроение)
- Персонализированные рекомендации на основе AI
- Визуальная аналитика с графиками прогресса
- База знаний: упражнения, продукты, статьи
- Экспорт данных в Excel и PDF

### Для администраторов:
- Кастомная админ-панель
- Управление пользователями
- CRUD для базы знаний (упражнения, продукты, статьи)
- Аналитика платформы
- Статистика использования

## Технологический стек

- **Backend**: Django 4.2.7
- **Frontend**: Django Templates + Bootstrap 5 + HTMX
- **База данных**: PostgreSQL
- **Кеширование**: Redis
- **Аналитика**: Pandas, NumPy
- **Визуализация**: Chart.js
- **Экспорт**: openpyxl, ReportLab

## Установка и запуск

### Предварительные требования

1. Python 3.10+
2. PostgreSQL 13+
3. Redis

### Шаг 1: Клонирование репозитория
```bash
git clone https://github.com/yourusername/fittracker.git
cd fittracker
```

### Шаг 2: Создание виртуального окружения
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Шаг 3: Установка зависимостей
```bash
pip install -r requirements.txt
```

### Шаг 4: Настройка базы данных PostgreSQL

Создайте базу данных:
```sql
CREATE DATABASE fittracker_db;
CREATE USER fittracker_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE fittracker_db TO fittracker_user;
```

### Шаг 5: Настройка переменных окружения

Создайте файл `.env` в корне проекта:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=django.db.backends.postgresql
DB_NAME=fittracker_db
DB_USER=fittracker_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

REDIS_URL=redis://127.0.0.1:6379/0
```

### Шаг 6: Создание папки для логов
```bash
mkdir logs
```

### Шаг 7: Миграции
```bash
python manage.py makemigrations
python manage.py migrate
```

### Шаг 8: Загрузка тестовых данных
```bash
python manage.py loaddata initial_data.json
```

### Шаг 9: Создание суперпользователя
```bash
python manage.py createsuperuser
```

### Шаг 10: Сбор статических файлов
```bash
python manage.py collectstatic --noinput
```

### Шаг 11: Запуск сервера разработки
```bash
python manage.py runserver
```

Приложение будет доступно по адресу: http://127.0.0.1:8000/

## Структура проекта
```
fittracker_project/
├── fittracker/              # Главный проект
├── users/                   # Пользователи и аутентификация
├── tracking/                # Трекинг питания и активности
├── recommendations/         # Система рекомендаций
├── analytics/              # Аналитика и экспорт
├── knowledge_base/         # База знаний
├── custom_admin/           # Кастомная админка
├── templates/              # HTML шаблоны
├── static/                 # Статические файлы
├── media/                  # Загруженные файлы
├── logs/                   # Логи приложения
└── manage.py
```

## Основные URL

- `/` - Главная страница (редирект на дашборд)
- `/register/` - Регистрация
- `/login/` - Вход
- `/dashboard/` - Дашборд пользователя
- `/food-logs/` - Журнал питания
- `/activity-logs/` - Журнал активности
- `/recommendations/` - Рекомендации
- `/analytics/` - Аналитика
- `/exercises/` - База упражнений
- `/foods/` - База продуктов
- `/admin/` - Кастомная админ-панель

## Git команды

### Инициализация репозитория
```bash
git init
git add .
git commit -m "Initial commit: FitTracker project setup"
```

### Создание удаленного репозитория
```bash
git remote add origin https://github.com/yourusername/fittracker.git
git branch -M main
git push -u origin main
```

### Работа с ветками
```bash
# Создать новую ветку
git checkout -b feature/new-feature

# Переключиться на ветку
git checkout main

# Слить ветку
git merge feature/new-feature

# Удалить ветку
git branch -d feature/new-feature
```

### Регулярные коммиты
```bash
git add .
git commit -m "Описание изменений"
git push
```

## Требования проекта

### Обязательные требования:
- ✅ Clean-code
- ✅ Качественный UI/UX
- ✅ Минимум 10 записей в БД
- ✅ Наследование шаблонов
- ✅ Адаптивный дизайн
- ✅ Регистрация + вход + выход
- ✅ Поиск
- ✅ Фильтрация
- ✅ Сортировка
- ✅ CRUD
- ✅ Валидация
- ✅ 3НФ базы данных
- ✅ Оптимизация запросов (select_related, values)
- ✅ Комментарии в коде
- ✅ Защита маршрутов
- ✅ Сессии (аккаунт не слетает)

### На "хорошо":
- ✅ Логгирование
- ✅ Пагинация

### На "отлично":
- ✅ Пагинация
- ✅ Диаграммы и статистика
- ✅ Экспорт в XLSX/PDF

## Лицензия

MIT License

## Автор

FitTracker Team

## Поддержка

При возникновении вопросов создайте issue в репозитории.