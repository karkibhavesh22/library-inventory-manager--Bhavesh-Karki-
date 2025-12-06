import json
from pathlib import Path
import logging
from typing import List, Optional
from .book import Book

logger = logging.getLogger(__name__)

class LibraryInventory:
    def __init__(self, storage_path: Path):
        self.storage_path = Path(storage_path)
        self.books: List[Book] = []
        self.load()

    def add_book(self, book: Book) -> None:
        if self.search_by_isbn(book.isbn):
            logger.info("Attempted to add duplicate ISBN: %s", book.isbn)
            raise ValueError("A book with this ISBN already exists.")
        self.books.append(book)
        logger.info("Book added: %s", book.isbn)
        self.save()

    def search_by_title(self, title: str) -> List[Book]:
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self) -> List[str]:
        return [str(b) for b in self.books]

    def save(self) -> None:
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            data = [b.to_dict() for b in self.books]
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            logger.info("Saved %d books to %s", len(self.books), self.storage_path)
        except Exception as e:
            logger.exception("Failed to save books: %s", e)
            raise

    def load(self) -> None:
        try:
            if not self.storage_path.exists():
                logger.info("Storage file does not exist; starting empty catalog.")
                self.books = []
                return
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.books = [Book(**item) for item in data]
            logger.info("Loaded %d books from %s", len(self.books), self.storage_path)
        except json.JSONDecodeError:
            logger.error("JSON file corrupted; starting with empty catalog.")
            self.books = []
        except Exception as e:
            logger.exception("Unexpected error loading books: %s", e)
            self.books = []
