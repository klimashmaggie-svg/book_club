from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.database import get_db, init_db
from app.models import Book, Club, User


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    seed_data()
    yield


app = FastAPI(
    title="BookClub API",
    version="0.1.0",
    description="Backend for the BookClub reader community service.",
    lifespan=lifespan,
)


def seed_data() -> None:
    from app.database import SessionLocal

    db = SessionLocal()
    try:
        if db.query(Book).count() == 0:
            from app.models import Author, Genre

            author = Author(name="Фёдор Достоевский", bio="Русский писатель и мыслитель.")
            genre = Genre(name="Классическая литература")
            db.add(author)
            db.add(genre)
            db.flush()

            book = Book(
                title="Преступление и наказание",
                description="Классический роман о морали, вине и искуплении.",
                cover_image="https://example.com/cover.jpg",
                published_year=1866,
                page_count=672,
                author_id=author.id,
                genre_id=genre.id,
            )
            db.add(book)

        if db.query(User).count() == 0:
            user = User(
                username="reader1",
                email="reader1@example.com",
                password_hash="hashed_password",
                role="member",
            )
            db.add(user)

        if db.query(Club).count() == 0:
            club = Club(
                name="Клуб классики",
                description="Обсуждаем произведения русской классики.",
                creator_id=1,
                genre_focus="Классическая литература",
                club_type="Общий",
            )
            db.add(club)

        db.commit()
    finally:
        db.close()


@app.get("/")
def read_root() -> dict:
    return {"status": "ok", "message": "BookClub API is running"}


@app.get("/api/books")
def list_books(db: Session = Depends(get_db)) -> list[dict]:
    books = db.query(Book).all()
    if not books:
        return []
    return [
        {
            "id": book.id,
            "title": book.title,
            "description": book.description,
            "author": book.author.name if book.author else None,
            "genre": book.genre.name if book.genre else None,
            "published_year": book.published_year,
            "page_count": book.page_count,
        }
        for book in books
    ]


@app.get("/api/clubs")
def list_clubs(db: Session = Depends(get_db)) -> list[dict]:
    clubs = db.query(Club).all()
    return [
        {
            "id": club.id,
            "name": club.name,
            "description": club.description,
            "creator_id": club.creator_id,
            "genre_focus": club.genre_focus,
            "club_type": club.club_type,
        }
        for club in clubs
    ]


@app.get("/api/users")
def list_users(db: Session = Depends(get_db)) -> list[dict]:
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
        }
        for user in users
    ]


@app.get("/health")
def health_check() -> dict:
    return {"status": "healthy"}
