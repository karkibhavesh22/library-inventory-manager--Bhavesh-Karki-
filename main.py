# cli/main.py
import sys
import os

# Add the project root to python path so we can import library_manager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from library_manager.book import Book
from library_manager.inventory import LibraryInventory

def print_menu():
    print("\n--- Library Management System ---")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search by Title")
    print("6. Exit")

def main():
    inventory = LibraryInventory("library.json")

    while True:
        print_menu()
        choice = input("Enter choice (1-6): ").strip()

        try:
            if choice == '1':
                title = input("Enter Title: ")
                author = input("Enter Author: ")
                isbn = input("Enter ISBN: ")
                try:
                    inventory.add_book(Book(title, author, isbn))
                    print("Book added successfully.")
                except ValueError as e:
                    print(f"Error: {e}")

            elif choice == '2':
                isbn = input("Enter ISBN to issue: ")
                book = inventory.search_by_isbn(isbn)
                if book and book.issue():
                    inventory.save_books()
                    print(f"You have issued: {book.title}")
                else:
                    print("Book not found or already issued.")

            elif choice == '3':
                isbn = input("Enter ISBN to return: ")
                book = inventory.search_by_isbn(isbn)
                if book and book.return_book():
                    inventory.save_books()
                    print(f"You have returned: {book.title}")
                else:
                    print("Book not found.")

            elif choice == '4':
                inventory.display_all()

            elif choice == '5':
                term = input("Enter title to search: ")
                results = inventory.search_by_title(term)
                if results:
                    for b in results: print(b)
                else:
                    print("No books found.")

            elif choice == '6':
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice, please try again.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()