from enum import Enum
from typing import Optional
from fastapi import FastAPI, Query, Path

app = FastAPI()

class BookGenre(str, Enum):
    FICTION = "Fiction"
    SCIENCE = "Science"
    HISTORY = "History"
    FANTASY = "Fantasy"

fake_books_db = [
    {"id": 1, "title": "The Hobbit", "genre": BookGenre.FANTASY},
    {"id": 2, "title": "A Brief History of Time", "genre": BookGenre.SCIENCE},
    {"id": 3, "title": "The Da Vinci Code", "genre": BookGenre.FICTION},
    {"id": 4, "title": "Sapiens: A Brief History of Humankind", "genre": BookGenre.HISTORY},
    {"id": 5, "title": "The Lord of the Rings", "genre": BookGenre.FANTASY},
    {"id": 6, "title": "To Kill a Mockingbird", "genre": BookGenre.FICTION},
    {"id": 7, "title": "The Selfish Gene", "genre": BookGenre.SCIENCE},
    {"id": 8, "title": "Guns, Germs, and Steel", "genre": BookGenre.HISTORY},
    {"id": 9, "title": "Harry Potter and the Sorcerer's Stone", "genre": BookGenre.FANTASY},
    {"id": 10, "title": "The Great Gatsby", "genre": BookGenre.FICTION},
    {"id": 11, "title": "Cosmos", "genre": BookGenre.SCIENCE},
    {"id": 12, "title": "The Silk Roads", "genre": BookGenre.HISTORY},
    {"id": 13, "title": "The Chronicles of Narnia", "genre": BookGenre.FANTASY},
    {"id": 14, "title": "1984", "genre": BookGenre.FICTION},
    {"id": 15, "title": "The Elegant Universe", "genre": BookGenre.SCIENCE},
    {"id": 16, "title": "SPQR: A History of Ancient Rome", "genre": BookGenre.HISTORY},
    {"id": 17, "title": "Percy Jackson & the Olympians", "genre": BookGenre.FANTASY},
    {"id": 18, "title": "Pride and Prejudice", "genre": BookGenre.FICTION},
    {"id": 19, "title": "A Short History of Nearly Everything", "genre": BookGenre.SCIENCE},
    {"id": 20, "title": "The Guns of August", "genre": BookGenre.HISTORY}
]

@app.get("/books")
def get_books(
    q: Optional[str] = Query(None, min_length=2),
    genre: Optional[BookGenre] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50)
):
    filtered_books = fake_books_db
    if q:
        filtered_books = [book for book in filtered_books if q.lower() in book["title"].lower()]
    if genre:
        filtered_books = [book for book in filtered_books if book["genre"] == genre]
    return filtered_books[skip : skip + limit]

@app.get("/books/stats")
def get_book_stats():
    total_books = len(fake_books_db)
    genre_counts = {genre.value: 0 for genre in BookGenre}
    for book in fake_books_db:
        genre_counts[book["genre"].value] += 1
    return {
        "total_books": total_books,
        "stats_by_genre": genre_counts
    }

@app.get("/books/{book_id}")
def get_book_by_id(
    book_id: int = Path(..., ge=1)
):
    for book in fake_books_db:
        if book["id"] == book_id:
            return book
    return {"error": "not found"}