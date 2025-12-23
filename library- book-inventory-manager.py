import json
import os

FILE_NAME = "library_data.json"


class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_issued = False

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "is_issued": self.is_issued
        }


class Library:
    def __init__(self, file_name):
        self.file_name = file_name
        self.books = {}  # HashMap-like dict
        self.load_books()

    def load_books(self):
        if not os.path.exists(self.file_name):
            return

        with open(self.file_name, "r") as file:
            data = json.load(file)
            for book_id, book_data in data.items():
                book = Book(
                    book_data["book_id"],
                    book_data["title"],
                    book_data["author"]
                )
                book.is_issued = book_data["is_issued"]
                self.books[book_id] = book

    def save_books(self):
        with open(self.file_name, "w") as file:
            json.dump(
                {bid: book.to_dict() for bid, book in self.books.items()},
                file,
                indent=4
            )

    def add_book(self, book_id, title, author):
        if book_id in self.books:
            print("Error: Book ID already exists.")
            return
        self.books[book_id] = Book(book_id, title, author)
        self.save_books()
        print("Book added successfully.")

    def search_by_title(self, title):
        results = [b for b in self.books.values()
                   if title.lower() in b.title.lower()]
        self.display_books(results)

    def search_by_author(self, author):
        results = [b for b in self.books.values()
                   if author.lower() in b.author.lower()]
        self.display_books(results)

    def issue_book(self, book_id):
        book = self.books.get(book_id)
        if not book:
            print("Book not found.")
            return
        if book.is_issued:
            print("Book already issued.")
            return
        book.is_issued = True
        self.save_books()
        print("Book issued successfully.")

    def return_book(self, book_id):
        book = self.books.get(book_id)
        if not book:
            print("Book not found.")
            return
        if not book.is_issued:
            print("Book was not issued.")
            return
        book.is_issued = False
        self.save_books()
        print("Book returned successfully.")

    def report(self):
        total = len(self.books)
        issued = sum(1 for b in self.books.values() if b.is_issued)
        print("\nLibrary Report")
        print("----------------")
        print(f"Total Books  : {total}")
        print(f"Issued Books : {issued}")

    def display_books(self, books):
        if not books:
            print("No books found.")
            return

        print("\n{:<8} {:<25} {:<20} {:<10}".format(
            "ID", "Title", "Author", "Status"))
        print("-" * 65)
        for b in books:
            status = "Issued" if b.is_issued else "Available"
            print("{:<8} {:<25} {:<20} {:<10}".format(
                b.book_id, b.title, b.author, status))


def main():
    library = Library(FILE_NAME)

    while True:
        print("\nLibrary Book Inventory Manager")
        print("1. Add Book")
        print("2. Search by Title")
        print("3. Search by Author")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. Report")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            bid = input("Book ID: ")
            title = input("Title: ")
            author = input("Author: ")
            library.add_book(bid, title, author)

        elif choice == "2":
            title = input("Enter title keyword: ")
            library.search_by_title(title)

        elif choice == "3":
            author = input("Enter author keyword: ")
            library.search_by_author(author)

        elif choice == "4":
            bid = input("Enter Book ID to issue: ")
            library.issue_book(bid)

        elif choice == "5":
            bid = input("Enter Book ID to return: ")
            library.return_book(bid)

        elif choice == "6":
            library.report()

        elif choice == "7":
            print("Exiting system.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
