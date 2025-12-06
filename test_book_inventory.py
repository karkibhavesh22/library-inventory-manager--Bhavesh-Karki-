import pytest
from library_manager.book import Book
from library_manager.inventory import LibraryInventory

def test_book_issue_return():
    b = Book("A", "Author", "ISBN1")
    assert b.is_available()
    assert b.issue() is True
    assert b.is_available() is False
    assert b.return_book() is True
    assert b.is_available() is True

def test_inventory_add_search_and_persistence(tmp_path):
    storage = tmp_path / "books.json"
    inv = LibraryInventory(storage)
    assert inv.books == []

    b = Book("Title1", "Auth", "ISBNX")
    inv.add_book(b)

    assert inv.search_by_isbn("ISBNX") is not None
    assert len(inv.search_by_title("title1")) > 0

    inv2 = LibraryInventory(storage)
    assert inv2.search_by_isbn("ISBNX") is not None

def test_duplicate_isbn_raises(tmp_path):
    storage = tmp_path / "books.json"
    inv = LibraryInventory(storage)
    b1 = Book("T1", "A", "DUPISBN")
    b2 = Book("T2", "B", "DUPISBN")
    inv.add_book(b1)
    with pytest.raises(ValueError):
        inv.add_book(b2)
