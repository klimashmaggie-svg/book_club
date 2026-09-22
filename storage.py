import json
from pathlib import Path

from models import Book, Club, Discussion, Member

DATA_DIR = Path("data")

# Пути к JSON-файлам с данными проекта.
BOOKS_FILE = DATA_DIR / "books.json"
MEMBERS_FILE = DATA_DIR / "members.json"
DISCUSSIONS_FILE = DATA_DIR / "discussions.json"
CLUBS_FILE = DATA_DIR / "clubs.json"


def load_all() -> tuple[
    list[Club],
    list[Member],
    list[Book],
    list[Discussion],
]:
    """Load all JSON data and convert dictionaries to objects."""
    # Сначала загружаются независимые сущности.
    members = [Member.from_data(item) for item in _read_json(MEMBERS_FILE)]
    books = [Book.from_data(item) for item in _read_json(BOOKS_FILE)]

    # Обсуждения зависят от книг и участников, поэтому создаются после них.
    discussions = [
        Discussion.from_data(item, books, members)
        for item in _read_json(DISCUSSIONS_FILE)
    ]

    # Клуб связывает участников, книги и обсуждения в одну модель.
    club_data = _read_json(CLUBS_FILE)
    clubs = [
        Club.from_data(item, members, books, discussions)
        for item in club_data
    ]
    clubs_by_id = {club.id: club for club in clubs}
    # После создания всех клубов восстанавливаем вложенность по id.
    for item, club in zip(club_data, clubs):
        club.subclubs = [
            clubs_by_id[club_id]
            for club_id in item.get("subclub_ids", [])
        ]
    return clubs, members, books, discussions


def save_all(
    clubs: list[Club],
    members: list[Member],
    books: list[Book],
    discussions: list[Discussion],
) -> None:
    """Save all objects to JSON files."""
    DATA_DIR.mkdir(exist_ok=True)

    # Перед сохранением объекты преобразуются в словари.
    _write_json(CLUBS_FILE, [club.to_data() for club in clubs])
    _write_json(MEMBERS_FILE, [member.to_data() for member in members])
    _write_json(BOOKS_FILE, [book.to_data() for book in books])
    _write_json(
        DISCUSSIONS_FILE,
        [discussion.to_data() for discussion in discussions],
    )


def _read_json(path: Path) -> list[dict]:
    # Если файла еще нет, считаем коллекцию пустой.
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as error:
        # Ошибка JSON превращается в понятное сообщение для проекта.
        raise ValueError(f"File {path} contains invalid JSON") from error


def _write_json(path: Path, data: list[dict]) -> None:
    # ensure_ascii=False сохраняет русские буквы в читаемом виде.
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
