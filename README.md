# Книжный клуб

Учебный проект на Python и Django. В проекте четыре сущности: клуб, участник,
книга и обсуждение. На этапе ПР7 веб-интерфейс получает данные из SQLite
через стандартный модуль Python `sqlite3` и SQL-запросы. JSON-файлы папки `data/`
сохранены для импорта и консольной версии. Django ORM пока не используется.

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
│   ├── bookclub.sqlite
│   ├── books.json
│   ├── clubs.json
│   ├── discussions.json
│   └── members.json
├── db/
│   ├── __init__.py
│   ├── database.py
│   └── import_json.py
├── sql/
│   ├── schema.sql
│   └── queries.sql
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
│   ├── test_database.py
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
- `data/` — SQLite-база сайта и исходные JSON-данные;
- `db/` — подключение SQLite, выполнение запросов и импорт JSON;
- `sql/` — схема таблиц и единый каталог SQL-запросов;
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
JSON-хранилище сохранены для консольной версии. С ПР7 все страницы сайта
читают отдельную SQLite-базу. Используются обычные GET-формы HTML;
классы Django Forms, ORM и пользовательская авторизация пока не применяются.

| Страница | URL | Назначение |
| --- | --- | --- |
| Главная | `/` | Описание проекта и общая статистика |
| Книги | `/books/` | Список всех книг |
| Книга | `/books/<id>/` | Информация о книге и отзывы |
| Подбор книги | `/books/unreviewed/?member=1` | Книги без отзыва участника |
| Клубы | `/clubs/` | Список книжных клубов |
| Клуб | `/clubs/<id>/` | Обсуждения выбранного клуба |
| Участники | `/members/` | Список участников |
| Участник | `/members/<id>/` | Данные участника и его отзывы |
| Отзывы | `/clubs/discussions/` | Список всех отзывов |
| Обсуждение | `/clubs/discussions/<id>/` | Участник, книга и текст отзыва |
| Статистика | `/clubs/statistics/?min_reviews=0` | COUNT, GROUP BY, HAVING |

Каждый адрес обрабатывается view-функцией. View вызывает `fetch_all()` или
`fetch_one()` из `db/database.py`; они выполняют SQL из `sql/queries.sql`.
Результаты `sqlite3.Row` передаются в шаблон через контекст. В JOIN-запросах
поля связанных таблиц называются `book_title`, `member_name`, `member_id`.
Отсутствующий объект даёт HTTP 404, пустая выборка — сообщение внутри страницы.

## Запуск в терминале VS Code

```bash
cd ~/Desktop/book_club
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python -m db.import_json
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
На ПР6 view-функции загружали объекты из JSON; с ПР7 они получают результаты
SQL-запросов. Затем формируют контекст и вызывают `render()`.
HTML в Python не формируется, функция `page()` не используется.

В проекте реализованы:

- базовый шаблон и наследование через `extends` и `block`;
- общая навигация и повторяющиеся карточки через `include`;
- вывод значений из контекста через `{{ ... }}`;
- циклы `for`, условия `if` и обработка пустых списков через `empty`;
- фильтры `length`, `default` и `stringformat`;
- именованные URL и пространства имён `homepage`, `books`, `clubs`;
- ссылки через тег `url`;
- CSS, JavaScript и PNG-изображение через систему `static`.

JSON-версия ПР6 сохранена в `models/`, `storage.py` и `main.py`.

## SQLite и SQL (ПР7)

### Схема и связи

База предметных данных: `data/bookclub.sqlite`. Отдельная `db.sqlite3`
по-прежнему предназначена для встроенных компонентов Django.
`manage.py migrate` не создаёт таблицы BookClub: для них нужен `sql/schema.sql`.

| Таблица | Поля и типы |
| --- | --- |
| `books` | `id INTEGER PRIMARY KEY`, `title TEXT`, `author TEXT`, `year INTEGER` |
| `members` | `id INTEGER PRIMARY KEY`, `name TEXT`, `email TEXT`, `role TEXT` |
| `clubs` | `id INTEGER PRIMARY KEY`, `name TEXT`, `description TEXT` |
| `discussions` | `id INTEGER PRIMARY KEY`, `book_id INTEGER`, `member_id INTEGER`, `review TEXT` |
| `club_discussions` | `club_id INTEGER`, `discussion_id INTEGER`, составной PRIMARY KEY |

Все поля, кроме автоматически задаваемых первичных ключей, объявлены NOT NULL.
`role` по умолчанию равна `reader`. Отсутствие отзыва представляется отсутствием
строки обсуждения; искусственные NULL-записи для этого не создаются.

`discussions.book_id` ссылается на `books.id`, `member_id` — на `members.id`.
Удаление книги или участника с отзывами запрещено (`RESTRICT`).
`club_discussions` связывает клуб и обсуждение: составной ключ предотвращает
дублирование пары, `CASCADE` удаляет только связи при удалении их владельцев.
Одно обсуждение может входить в несколько клубов.

### Подготовка и повторный импорт

```bash
# Создание схемы и импорт существующих данных одной командой:
.venv/bin/python -m db.import_json

# Только создание таблиц (без импорта):
sqlite3 data/bookclub.sqlite < sql/schema.sql
```

Первый импорт даёт 7 книг, 5 участников, 3 клуба, 3 обсуждения и 3 связи.
Повторный запуск не создаёт дубликаты и не перезаписывает изменения SQLite.
Чтобы явно обновить существующие записи из JSON и заменить состав обсуждений
импортируемых клубов, используйте:

```bash
.venv/bin/python -m db.import_json --update-existing
```

Эта команда не удаляет дополнительные объекты SQLite, которых нет в JSON.
Импорт выполняется одной транзакцией: при ошибке данных/связей все изменения
импорта откатываются. JSON-файлы не изменяются. Сайт ничего не импортирует
автоматически: изменения записей SQLite видны на следующем запросе страницы.

### Подключение и запросы

`db/database.py` строит абсолютный путь к базе, включает `PRAGMA foreign_keys = ON`
для каждого подключения и устанавливает `row_factory = sqlite3.Row`.
Соединения закрываются через `contextlib.closing`; параметры передаются отдельно
от SQL через `?`. При отсутствии файла выводится инструкция запустить импорт,
а пустая база вместо нужного файла незаметно не создаётся.

В `sql/queries.sql` содержится 18 запросов. Метки `-- name:` используются
`get_queries()` для загрузки команд из этого же файла, без копирования SQL во view.
Все запросы используются в веб-сценариях:

| Запросы | Назначение и страница |
| --- | --- |
| `books`, `search_books` | Каталог `/books/`, поиск по названию/автору и году |
| `members`, `members_by_role` | Участники `/members/`, отбор по роли |
| `discussions` | JOIN книг и участников, `/clubs/discussions/`, фильтр по клубу |
| `book_discussions`, `member_discussions` | JOIN для отзывов книги/участника |
| `book_totals`, `community_totals` | COUNT, MIN, MAX для главной и статистики |
| `book_statistics` | LEFT JOIN, GROUP BY, HAVING: количество отзывов по книгам |
| `clubs`, `member_statistics` | GROUP BY: обсуждения клубов и отзывы участников |
| `unreviewed_books` | NOT EXISTS: книги без отзыва выбранного участника |
| `book`, `member`, `club`, `discussion` | Детальные страницы, поиск по id |
| `featured_discussions` | JOIN, ORDER BY, LIMIT/OFFSET: три отзыва на главной |

Есть не менее двух списочных, фильтрующих, JOIN-, агрегатных и группирующих
запросов. `LEFT JOIN` сохраняет нулевые показатели, `HAVING` отбирает группы,
`COUNT(d.id)` не считает пустые строки LEFT JOIN как отзывы.

### Пользовательские сценарии

1. `/books/` — каталог SQLite с поиском `q` и нижней границей года `year`.
2. `/members/?role=moderator` — участники заданной роли (WHERE).
3. `/clubs/discussions/?club=2` — отзывы выбранного клуба со связанными данными.
4. `/books/unreviewed/?member=1` — книги, о которых участник ещё не писал;
   дополнительный параметр `q` ограничивает название/автора.
5. `/clubs/statistics/?min_reviews=1` — статистика с порогом HAVING.
6. `/books/1/`, `/members/1/`, `/clubs/1/` и страницы отзывов — связанные записи.

Поиск книг без отзыва участника — адаптация учебного поиска свободного
помещения к BookClub. Дат бронирования в этой предметной области нет.
Параметры берутся из GET, проверяются и передаются в SQL отдельно.
Неверный год/идентификатор даёт понятное сообщение; пустые результаты — empty.
Поиск текста через `instr(lower(...), lower(?))` буквальный: `%` и `_` не
являются масками. Стандартная SQLite приводит регистр ASCII, поэтому для
русского текста вводите фрагмент в том же регистре, что в каталоге.

### Проверка SQL и сайта

```bash
sqlite3 data/bookclub.sqlite
```

В CLI можно выполнить весь каталог. Сначала задайте параметры: без них
LIMIT/OFFSET получат NULL и SQLite выдаст ошибку datatype mismatch.
Значения 1 и 0 подходят для пробного выполнения всех команд:

```sql
.tables
PRAGMA foreign_key_check;
SELECT COUNT(*) FROM books;
SELECT COUNT(*) FROM members;
SELECT COUNT(*) FROM discussions;
.parameter init
.parameter set ?1 1
.parameter set ?2 0
.read sql/queries.sql
.quit
```

Проверьте обновление данных: `UPDATE books SET title = 'Проверка' WHERE id = 1;`,
обновите `/books/1/`, затем верните название. Проверка `sqlite3.Row`, повторного
импорта, отката, фильтров, JOIN, статистики, инъекций и SQL-источника страниц
выполняется тестами на временной базе, не затрагивая рабочую.

```bash
.venv/bin/python manage.py check
.venv/bin/python -m pytest -v
.venv/bin/python -m flake8 .
```

ПР7 фиксируется Git-коммитом с префиксом `PR7:`. Изучение материалов
Яндекс Практикума подтверждается отдельно в личном кабинете; репозиторий
содержит реализацию индивидуального проекта, а не подтверждение прохождения курса.
