"""Перенос исходных JSON в SQLite: python -m db.import_json."""

import argparse
import json
from contextlib import closing
from pathlib import Path

from db.database import ROOT, get_connection, initialize_database

DATA_DIR = ROOT / "data"


def read_json(data_dir: Path, name: str) -> list[dict]:
    """Проверить коллекцию и уникальность идентификаторов перед импортом."""
    with (data_dir / f"{name}.json").open(encoding="utf-8") as source:
        records = json.load(source)
    if not isinstance(records, list):
        raise ValueError(f"{name}.json должен содержать список")
    ids = [record["id"] for record in records]
    if len(ids) != len(set(ids)):
        raise ValueError(f"Повтор идентификаторов в {name}.json")
    return records


def import_data(
    data_dir: Path = DATA_DIR,
    db_path: Path | None = None,
    update_existing: bool = False,
) -> dict[str, int]:
    """Импортировать всё одной транзакцией, не меняя JSON и текущие записи."""
    books = read_json(data_dir, "books")
    members = read_json(data_dir, "members")
    clubs = read_json(data_dir, "clubs")
    discussions = read_json(data_dir, "discussions")
    initialize_database(db_path)

    # Порядок учитывает внешние ключи. Ошибка отменяет весь импорт.
    with closing(get_connection(db_path)) as connection:
        with connection:
            collections = (
                ("books", ("id", "title", "author", "year"), books),
                ("members", ("id", "name", "email", "role"), [
                    {**item, "role": item.get("role", "reader")}
                    for item in members
                ]),
                ("clubs", ("id", "name", "description"), clubs),
                ("discussions", ("id", "book_id", "member_id", "review"),
                 discussions),
            )
            for table, columns, records in collections:
                # Имена таблиц/полей заданы кодом; только значения идут через ?.
                placeholders = ", ".join("?" for _ in columns)
                conflict = "DO NOTHING"
                if update_existing:
                    assignments = ", ".join(
                        f"{column} = excluded.{column}" for column in columns[1:]
                    )
                    conflict = f"DO UPDATE SET {assignments}"
                connection.executemany(
                    f"INSERT INTO {table} ({', '.join(columns)}) "
                    f"VALUES ({placeholders}) ON CONFLICT(id) {conflict}",
                    [tuple(record[column] for column in columns)
                     for record in records],
                )
            if update_existing:
                connection.executemany(
                    "DELETE FROM club_discussions WHERE club_id = ?",
                    [(club["id"],) for club in clubs],
                )
            connection.executemany(
                "INSERT INTO club_discussions (club_id, discussion_id) "
                "VALUES (?, ?) ON CONFLICT(club_id, discussion_id) DO NOTHING",
                [(club["id"], discussion_id) for club in clubs
                 for discussion_id in club.get("discussion_ids", [])],
            )
            counts = {
                table: connection.execute(
                    f"SELECT COUNT(*) FROM {table}"
                ).fetchone()[0]
                for table in (
                    "books", "members", "clubs", "discussions", "club_discussions"
                )
            }
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description="Импорт JSON в SQLite BookClub")
    parser.add_argument(
        "--update-existing", action="store_true",
        help="Обновить записи и состав обсуждений клубов значениями из JSON",
    )
    args = parser.parse_args()
    for table, count in import_data(update_existing=args.update_existing).items():
        print(f"{table}: {count}")


if __name__ == "__main__":
    main()
