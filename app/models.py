from __future__ import annotations

import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(30), default="member")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    club_memberships: Mapped[list[ClubMember]] = relationship(back_populates="user")
    favorites: Mapped[list[Favorite]] = relationship(back_populates="user")
    reading_progress: Mapped[list[ReadingProgress]] = relationship(back_populates="user")
    reviews: Mapped[list[Review]] = relationship(back_populates="user")
    discussions: Mapped[list[Discussion]] = relationship(back_populates="user")
    comments: Mapped[list[Comment]] = relationship(back_populates="user")
    clubs_created: Mapped[list[Club]] = relationship(back_populates="creator")


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    photo: Mapped[str | None] = mapped_column(String(255), nullable=True)

    books: Mapped[list[Book]] = relationship(back_populates="author")


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    books: Mapped[list[Book]] = relationship(back_populates="genre")


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    cover_image: Mapped[str | None] = mapped_column(String(255), nullable=True)
    published_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    page_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    author_id: Mapped[int | None] = mapped_column(ForeignKey("authors.id"), nullable=True)
    genre_id: Mapped[int | None] = mapped_column(ForeignKey("genres.id"), nullable=True)

    author: Mapped[Author | None] = relationship(back_populates="books")
    genre: Mapped[Genre | None] = relationship(back_populates="books")
    favorites: Mapped[list[Favorite]] = relationship(back_populates="book")
    reading_progress: Mapped[list[ReadingProgress]] = relationship(back_populates="book")
    reviews: Mapped[list[Review]] = relationship(back_populates="book")
    club_books: Mapped[list[ClubBook]] = relationship(back_populates="book")


class Club(Base):
    __tablename__ = "clubs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    genre_focus: Mapped[str | None] = mapped_column(String(100), nullable=True)
    club_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    creator: Mapped[User] = relationship(back_populates="clubs_created")
    members: Mapped[list[ClubMember]] = relationship(back_populates="club")
    discussions: Mapped[list[Discussion]] = relationship(back_populates="club")
    club_books: Mapped[list[ClubBook]] = relationship(back_populates="club")


class ClubMember(Base):
    __tablename__ = "club_members"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    club_id: Mapped[int] = mapped_column(ForeignKey("clubs.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    joined_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    club: Mapped[Club] = relationship(back_populates="members")
    user: Mapped[User] = relationship(back_populates="club_memberships")


class ClubBook(Base):
    __tablename__ = "club_books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    club_id: Mapped[int] = mapped_column(ForeignKey("clubs.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))

    club: Mapped[Club] = relationship(back_populates="club_books")
    book: Mapped[Book] = relationship(back_populates="club_books")


class Discussion(Base):
    __tablename__ = "discussions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    club_id: Mapped[int] = mapped_column(ForeignKey("clubs.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    club: Mapped[Club] = relationship(back_populates="discussions")
    user: Mapped[User] = relationship(back_populates="discussions")
    comments: Mapped[list[Comment]] = relationship(back_populates="discussion")


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    discussion_id: Mapped[int] = mapped_column(ForeignKey("discussions.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    discussion: Mapped[Discussion] = relationship(back_populates="comments")
    user: Mapped[User] = relationship(back_populates="comments")


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    rating: Mapped[int] = mapped_column(Integer)
    review_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    book: Mapped[Book] = relationship(back_populates="reviews")
    user: Mapped[User] = relationship(back_populates="reviews")


class Favorite(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="favorites")
    book: Mapped[Book] = relationship(back_populates="favorites")


class ReadingProgress(Base):
    __tablename__ = "reading_progress"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    pages_read: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(50), default="want_to_read")
    started_at: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    user: Mapped[User] = relationship(back_populates="reading_progress")
    book: Mapped[Book] = relationship(back_populates="reading_progress")
