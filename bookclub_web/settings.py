"""
Настройки Django-проекта bookclub_web.

Файл создан командой django-admin startproject в Django 5.2.17.

Описание настройки проекта:
https://docs.djangoproject.com/en/5.2/topics/settings/

Полный список настроек и их значений:
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path

# Корень проекта: от него строятся пути к templates и базе SQLite.
BASE_DIR = Path(__file__).resolve().parent.parent


# Настройки для локальной разработки; перед публикацией их нужно пересмотреть.
# Порядок подготовки: https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# Ключ для криптографической подписи Django. На публичном сервере хранится в секрете.
SECRET_KEY = "django-insecure-x&f80k6n^^0xhpctb82suj&-fv+=0+y23@(1#zua9p%s#dprsh"

# Подробные страницы ошибок для разработки. На публичном сервере ставится False.
DEBUG = True

# Разрешённые имена хостов: локальный браузер и тестовый клиент Django.
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "testserver"]


# Регистрация встроенных приложений Django и приложений BookClub.

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "homepage",
    "books",
    "clubs",
]

# Обработчики запросов и ответов: безопасность, сессии, CSRF и авторизация.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Главный файл маршрутов: подключает адреса приложений.
ROOT_URLCONF = "bookclub_web.urls"

# Настройки обработки HTML-шаблонов Django.
TEMPLATES = [
    {
        # Шаблонизатор, обрабатывающий теги block, include, for и другие.
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Общая папка с base.html и навигацией.
        'DIRS': [BASE_DIR / "templates"],
        # Дополнительно искать шаблоны в папках templates приложений.
        'APP_DIRS': True,
        'OPTIONS': {
            # Добавлять в контекст запрос, пользователя и сообщения Django.
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Точка входа для серверов, поддерживающих интерфейс WSGI.
WSGI_APPLICATION = 'bookclub_web.wsgi.application'


# Служебная база SQLite для Django. Предметные данные пока хранятся в data/*.json.
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        # Тип базы данных и путь к её файлу.
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Проверки паролей для встроенной системы пользователей Django.
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        # Пароль не должен быть слишком похож на данные пользователя.
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        # Проверка минимальной длины пароля.
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        # Запрет слишком распространённых паролей.
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # Запрет паролей, состоящих только из цифр.
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Язык интерфейса Django и работа со временем.
# https://docs.djangoproject.com/en/5.2/topics/i18n/

# Русский язык встроенных сообщений Django.
LANGUAGE_CODE = "ru-RU"

# Часовой пояс для локального отображения времени.
TIME_ZONE = "Europe/Moscow"

# Включить поддержку перевода сообщений.
USE_I18N = True

# Использовать даты и время с информацией о часовом поясе.
USE_TZ = True


# Статические файлы: CSS, JavaScript и изображения.
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# Префикс URL для статических файлов, например /static/homepage/css/style.css.
STATIC_URL = "static/"

# Тип автоматически создаваемого первичного ключа будущих ORM-моделей.
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
