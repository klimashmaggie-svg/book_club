-- Структура базы BookClub. Запускать из корня проекта:
-- sqlite3 data/bookclub.sqlite < sql/schema.sql

-- Проверка внешних ключей включается для каждого подключения отдельно.
PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

-- Книга: идентификатор, название, автор и год издания.
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER NOT NULL
);

-- Участник: имя, почта и роль из существующей модели Member.
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'reader'
);

-- Клуб: название и описание. Обсуждения связаны отдельной таблицей ниже.
CREATE TABLE IF NOT EXISTS clubs (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL
);

-- Обсуждение объединяет существующую книгу, участника и текст отзыва.
-- RESTRICT запрещает удалять книгу или участника, пока на них ссылается отзыв.
CREATE TABLE IF NOT EXISTS discussions (
    id INTEGER PRIMARY KEY,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    review TEXT NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books (id) ON DELETE RESTRICT,
    FOREIGN KEY (member_id) REFERENCES members (id) ON DELETE RESTRICT
);

-- Связь клуба с его обсуждениями. Составной ключ исключает повтор пары.
-- CASCADE удаляет связь при удалении клуба или обсуждения.
CREATE TABLE IF NOT EXISTS club_discussions (
    club_id INTEGER NOT NULL,
    discussion_id INTEGER NOT NULL,
    PRIMARY KEY (club_id, discussion_id),
    FOREIGN KEY (club_id) REFERENCES clubs (id) ON DELETE CASCADE,
    FOREIGN KEY (discussion_id) REFERENCES discussions (id) ON DELETE CASCADE
);

COMMIT;
