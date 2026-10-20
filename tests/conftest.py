"""Добавляет корень проекта в путь импорта для запуска pytest."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def sqlite_db(tmp_path, monkeypatch):
    """Каждый SQL/веб-тест получает отдельную базу, не затрагивая данные сайта."""
    from db import database
    from db.import_json import import_data

    path = tmp_path / "bookclub.sqlite"
    import_data(db_path=path)
    monkeypatch.setattr(database, "DB_PATH", path)
    return path
