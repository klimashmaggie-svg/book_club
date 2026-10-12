# Книжный клуб

Учебный проект на Python и Django. В проекте четыре сущности: клуб, участник,
книга и обсуждение. Данные хранятся в JSON-файлах папки `data/`, а Django
предоставляет веб-интерфейс для их просмотра.

## Данные

В примере созданы 5 участников, 7 книг, 3 обсуждения и 3 клуба. Обсуждение объединяет участника, книгу и его отзыв. Клуб хранит список объектов обсуждений.

## Структура

```text
book_club/
├── bookclub_web/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── homepage/
│   ├── templates/
│   ├── static/homepage/
│   ├── urls.py
│   └── views.py
├── books/
│   ├── templates/
│   ├── urls.py
│   └── views.py
├── clubs/
│   ├── templates/
│   ├── urls.py
│   └── views.py
├── data/
│   ├── books.json
│   ├── clubs.json
│   ├── discussions.json
│   └── members.json
├── models/
│   ├── __init__.py
│   ├── book.py
│   ├── club.py
│   ├── discussion.py
│   └── member.py
├── tests/
│   ├── conftest.py
│   ├── test_book.py
│   ├── test_club_discussion.py
│   ├── test_member.py
│   ├── test_storage.py
│   └── test_web.py
├── templates/
│   ├── includes/navigation.html
│   └── base.html
├── .flake8
├── .gitignore
├── manage.py
├── main.py
├── README.md
├── requirements.txt
└── storage.py
```


Назначение основных частей:

- `models/member.py` — класс участника, роли, добавление и поиск;
- `models/book.py` — класс книги, добавление и поиск;
- `models/discussion.py` — объект, объединяющий участника, книгу и отзыв;
- `models/club.py` — клуб, который хранит список обсуждений;
- `bookclub_web/` — настройки и корневая маршрутизация Django;
- `homepage/` — главная страница, участники и статические файлы;
- `books/` — список книг и страница отдельной книги;
- `clubs/` — список клубов, страницы клуба и обсуждения;
- `data/` — исходные данные проекта в формате JSON;
- `storage.py` — чтение JSON, создание связанных объектов и сохранение;
- `main.py` — точка входа и вывод результатов в терминал;
- `tests/` — автоматические тесты классов, связей и хранилища;
- `manage.py` — управление Django-проектом и запуск development-сервера;
- `requirements.txt` — зависимости для запуска и проверки проекта;
- `.flake8` — настройки проверки оформления кода.

## Логика проекта и связи объектов

```text
Club
└── discussions: list[Discussion]
    └── Discussion
        ├── member: Member
        ├── book: Book
        └── review: str
```

Основная логика проекта строится следующим образом:

1. `Member` представляет участника книжного клуба.
2. `Book` представляет книгу.
3. Участник пишет отзыв о книге. Объекты `Member`, `Book` и текст отзыва
   объединяются в объекте `Discussion`.
4. `Club` хранит список объектов `Discussion`.

Создание связи в Python:

```python
discussion = Discussion(
    discussion_id=1,
    member=member,
    book=book,
    review="Интересная книга.",
)

club.add_discussion(discussion)
```

После этого через обсуждение доступны связанные данные:

```python
discussion.member.name
discussion.book.title
discussion.review
```

Через клуб можно получить все входящие в него обсуждения:

```python
for discussion in club.discussions:
    print(discussion)
```

### Связи в JSON

В программе связи представлены объектами. В JSON вместо объектов сохраняются
их идентификаторы.

Обсуждение хранит идентификаторы участника и книги:

```json
{
  "id": 1,
  "member_id": 1,
  "book_id": 1,
  "review": "Интересная книга."
}
```

Клуб хранит идентификаторы обсуждений:

```json
{
  "id": 1,
  "name": "Клуб классики",
  "description": "Отзывы о классической литературе.",
  "discussion_ids": [1]
}
```

Функция `load_all()` сначала создаёт участников и книги, затем связывает их с
обсуждениями по `member_id` и `book_id`. После этого обсуждения добавляются в
клубы по `discussion_ids`. Функция `save_all()` выполняет обратное
преобразование и записывает данные в JSON.

## Что за что отвечает

### `models/book.py`

Класс `Book` описывает книгу:

- `id` — идентификатор;
- `title` — название;
- `author` — автор;
- `year` — год издания;
- `matches_query()` — проверяет совпадение с поисковым запросом;
- `to_data()` и `from_data()` — преобразуют книгу для JSON и обратно.

### `models/member.py`

Класс `Member` описывает участника:

- `id` — идентификатор;
- `name` — имя;
- `email` — электронная почта;
- `role` — роль в проекте;
- `is_moderator` — показывает, может ли участник быть модератором;
- `to_data()` и `from_data()` — преобразуют участника для JSON и обратно.

### `models/discussion.py`

Класс `Discussion` объединяет три значения:

- `member` — объект участника, который оставил отзыв;
- `book` — объект книги, о которой написан отзыв;
- `review` — текст отзыва;
- `is_about()` — проверяет связь обсуждения с книгой;
- `to_data()` и `from_data()` — сохраняют и восстанавливают связи по id.

### `models/club.py`

Класс `Club` хранит список объектов `Discussion`:

- `discussions` — обсуждения клуба;
- `add_discussion()` — добавляет готовое обсуждение;
- `create_discussion()` — создаёт обсуждение и добавляет его в клуб;
- `to_data()` и `from_data()` — сохраняют и восстанавливают список обсуждений.

### `storage.py`

- `load_all()` читает JSON-файлы, создаёт объекты и восстанавливает связи;
- `save_all()` преобразует объекты в словари и записывает их в JSON.

### `main.py`

Запускает программу, загружает данные, выводит клубы, обсуждения, участников и
книги, показывает примеры поиска и сохраняет данные.

### `data/`

- `books.json` — книги;
- `members.json` — участники;
- `discussions.json` — связи участников, книг и отзывов;
- `clubs.json` — клубы и идентификаторы входящих в них обсуждений.

### `tests/`

Содержит тесты создания объектов, поиска, связей между объектами, загрузки и
сохранения JSON, а также Django-страниц и ответов HTTP 404.

## Веб-интерфейс Django

На ПР5 поверх консольного проекта добавлен веб-слой. Классы из `models/` и
JSON-хранилище продолжают использоваться. Django ORM, формы и авторизация на
этом этапе не применяются.

| Страница | URL | Назначение |
| --- | --- | --- |
| Главная | `/` | Описание проекта и общая статистика |
| Книги | `/books/` | Список всех книг |
| Книга | `/books/<id>/` | Информация о книге и отзывы |
| Клубы | `/clubs/` | Список книжных клубов |
| Клуб | `/clubs/<id>/` | Обсуждения выбранного клуба |
| Участники | `/members/` | Список участников |
| Участник | `/members/<id>/` | Данные участника и его отзывы |
| Отзывы | `/clubs/discussions/` | Список всех отзывов |
| Обсуждение | `/clubs/discussions/<id>/` | Участник, книга и текст отзыва |

Каждый адрес обрабатывается view-функцией. View вызывает `load_all()`, получает
объекты, передаёт их в HTML-шаблон и возвращает HTTP-ответ. Если объект с
указанным id отсутствует, возвращается ответ HTTP 404.

## Запуск в терминале VS Code

```bash
cd ~/Desktop/book_club
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py migrate
```

Запуск консольной версии:

```bash
.venv/bin/python main.py
```

Запуск Django:

```bash
.venv/bin/python manage.py runserver
```

После запуска веб-интерфейс доступен по адресу `http://127.0.0.1:8000/`.

Если виртуальное окружение уже создано и зависимости установлены, создавать
его повторно не нужно.

Проверка тестов и стиля:

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m flake8 .
.venv/bin/python manage.py check
```

## Основные Django-файлы

- `manage.py` — запуск команд и development-сервера Django;
- `bookclub_web/settings.py` — настройки, приложения и локализация;
- `bookclub_web/urls.py` — корневая маршрутизация;
- `bookclub_web/asgi.py`, `bookclub_web/wsgi.py` — серверные точки входа;
- `homepage/views.py` — главная страница и страницы участников;
- `homepage/urls.py` — адреса `/`, `/members/` и `/members/<id>/`;
- `templates/base.html` — общий HTML-каркас всех страниц;
- `templates/includes/navigation.html` — общая навигация через `include`;
- `homepage/templates/homepage/` — главная и страницы участников;
- `books/templates/books/` — список и подробная страница книги;
- `clubs/templates/clubs/` — страницы клубов и обсуждений;
- `homepage/static/homepage/css/style.css` — собственное оформление;
- `homepage/static/homepage/js/main.js` — текущий год и активный пункт меню;
- `homepage/static/homepage/img/logo.png` — графический логотип;
- `tests/test_web.py` — страницы, динамические маршруты и ответы 404.

## Шаблоны Django (ПР6)

Веб-интерфейс построен по схеме `View -> Context -> Template -> HTML`.
View-функции загружают объекты из JSON, формируют словарь контекста и вызывают
`render()`. HTML в Python не формируется, функция `page()` не используется.

В проекте реализованы:

- базовый шаблон и наследование через `extends` и `block`;
- общая навигация и повторяющиеся карточки через `include`;
- вывод значений из контекста через `{{ ... }}`;
- циклы `for`, условия `if` и обработка пустых списков через `empty`;
- фильтры `length`, `default` и `stringformat`;
- именованные URL и пространства имён `homepage`, `books`, `clubs`;
- ссылки через тег `url`;
- CSS, JavaScript и PNG-изображение через систему `static`.

Предметные данные продолжают храниться в JSON. Django ORM, формы и
авторизация на этапе ПР6 не используются.
