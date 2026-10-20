-- Именованные SELECT-запросы веб-приложения (ПР7).
-- Метка -- name: позволяет Python загрузить команду из этого же файла.
-- Значения ? передаются отдельно. Для CLI можно задать, например:
-- .parameter init
-- .parameter set ?1 1
-- .parameter set ?2 0

-- 1. SELECT: каталог книг с устойчивой сортировкой.
-- name: books
SELECT id, title, author, year FROM books ORDER BY title, id;

-- 2. SELECT: список участников, включая выбранные роли.
-- name: members
SELECT id, name, email, role FROM members ORDER BY name, id;

-- 3. WHERE: текст названия/автора и нижняя граница года. Параметры: текст, год.
-- instr ищет буквальный текст: %, _ не являются шаблонами LIKE.
-- lower SQLite учитывает регистр ASCII; для кириллицы поиск регистрозависим.
-- name: search_books
SELECT id, title, author, year FROM books
WHERE (instr(lower(title), lower(?1)) > 0
       OR instr(lower(author), lower(?1)) > 0)
  AND (?2 IS NULL OR year >= ?2)
ORDER BY title, id;

-- 4. WHERE: отбор участников по роли (owner, moderator, reader).
-- name: members_by_role
SELECT id, name, email, role FROM members WHERE role = ? ORDER BY name, id;

-- 5. JOIN: список отзывов с книгой и автором. Параметр: id клуба либо NULL.
-- EXISTS не размножает отзывы, если обсуждение входит в несколько клубов.
-- name: discussions
SELECT d.id, d.review, b.id AS book_id, b.title AS book_title,
       m.id AS member_id, m.name AS member_name, m.email AS member_email
FROM discussions AS d
JOIN books AS b ON b.id = d.book_id
JOIN members AS m ON m.id = d.member_id
WHERE (?1 IS NULL OR EXISTS (
    SELECT 1 FROM club_discussions AS cd
    WHERE cd.discussion_id = d.id AND cd.club_id = ?1
))
ORDER BY d.id;

-- 6. JOIN: отзывы выбранной книги с именами участников.
-- name: book_discussions
SELECT d.id, d.review, b.id AS book_id, b.title AS book_title,
       m.id AS member_id, m.name AS member_name, m.email AS member_email
FROM discussions AS d
JOIN books AS b ON b.id = d.book_id
JOIN members AS m ON m.id = d.member_id
WHERE d.book_id = ? ORDER BY d.id;

-- 7. Агрегаты: количество книг и границы годов для статистики.
-- name: book_totals
SELECT COUNT(*) AS books_count, MIN(year) AS earliest_year,
       MAX(year) AS latest_year FROM books;

-- 8. Агрегаты: общая численность сообщества и отзывов.
-- name: community_totals
SELECT (SELECT COUNT(*) FROM members) AS members_count,
       (SELECT COUNT(*) FROM clubs) AS clubs_count,
       (SELECT COUNT(*) FROM discussions) AS discussions_count;

-- 9. GROUP BY + HAVING: книги с числом отзывов не ниже порога (?1).
-- LEFT JOIN включает книги без отзывов при пороге 0.
-- name: book_statistics
SELECT b.id, b.title, COUNT(d.id) AS discussion_count
FROM books AS b LEFT JOIN discussions AS d ON d.book_id = b.id
GROUP BY b.id, b.title HAVING COUNT(d.id) >= ?
ORDER BY discussion_count DESC, b.title, b.id;

-- 10. GROUP BY: клубы и количество их обсуждений, включая пустые клубы.
-- name: clubs
SELECT c.id, c.name, c.description, COUNT(cd.discussion_id) AS discussion_count
FROM clubs AS c LEFT JOIN club_discussions AS cd ON cd.club_id = c.id
GROUP BY c.id, c.name, c.description ORDER BY c.id;

-- 11. NOT EXISTS: книги, о которых участник ещё не писал. Параметры: id, текст.
-- name: unreviewed_books
SELECT b.id, b.title, b.author, b.year FROM books AS b
WHERE NOT EXISTS (
    SELECT 1 FROM discussions AS d
    WHERE d.book_id = b.id AND d.member_id = ?1
)
AND (instr(lower(b.title), lower(?2)) > 0
     OR instr(lower(b.author), lower(?2)) > 0)
ORDER BY b.title, b.id;

-- 12. Одна книга для детальной страницы; отсутствие даёт пустой результат.
-- name: book
SELECT id, title, author, year FROM books WHERE id = ?;

-- 13. Один участник для детальной страницы.
-- name: member
SELECT id, name, email, role FROM members WHERE id = ?;

-- 14. Один клуб для страницы его обсуждений.
-- name: club
SELECT id, name, description FROM clubs WHERE id = ?;

-- 15. JOIN: полные данные одного отзыва.
-- name: discussion
SELECT d.id, d.review, b.id AS book_id, b.title AS book_title,
       m.id AS member_id, m.name AS member_name, m.email AS member_email
FROM discussions AS d
JOIN books AS b ON b.id = d.book_id
JOIN members AS m ON m.id = d.member_id WHERE d.id = ?;

-- 16. JOIN: все отзывы конкретного участника.
-- name: member_discussions
SELECT d.id, d.review, b.id AS book_id, b.title AS book_title,
       m.id AS member_id, m.name AS member_name, m.email AS member_email
FROM discussions AS d
JOIN books AS b ON b.id = d.book_id
JOIN members AS m ON m.id = d.member_id
WHERE d.member_id = ? ORDER BY d.id;

-- 17. LIMIT/OFFSET: небольшой блок отзывов на главной. Параметры: лимит, сдвиг.
-- В модели пока нет даты, поэтому сохраняется порядок по id.
-- name: featured_discussions
SELECT d.id, d.review, b.title AS book_title, m.name AS member_name
FROM discussions AS d
JOIN books AS b ON b.id = d.book_id
JOIN members AS m ON m.id = d.member_id
ORDER BY d.id LIMIT ? OFFSET ?;

-- 18. GROUP BY: статистика авторов отзывов, включая участников без отзывов.
-- name: member_statistics
SELECT m.id, m.name, COUNT(d.id) AS discussion_count
FROM members AS m LEFT JOIN discussions AS d ON d.member_id = m.id
GROUP BY m.id, m.name ORDER BY discussion_count DESC, m.name, m.id;
