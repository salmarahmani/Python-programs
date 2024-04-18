"""
This Python program represents a simple library management system using SQLite for data storage and CSV files for data export. It defines classes for Book, Borrower, and Library, each encapsulating functionalities related to managing books, borrowers, and library operations, respectively. The Library class interacts with the SQLite database to perform operations such as adding, removing, borrowing, and returning books, as well as managing borrowers. Additionally, the program provides options to search for books, display all books, search for borrowed books by a specific borrower, and export library data to CSV files. Users interact with the library through a command-line interface that offers various options for managing library resources.
"""

import sqlite3
import csv

class Book:
    def __init__(self, book_id, title, author, year, available=True):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.available = available

class Borrower:
    def __init__(self, name, borrower_id):
        self.name = name
        self.borrower_id = borrower_id
        self.borrow_history = []

class Library:
    def __init__(self):
        self.conn = sqlite3.connect('library.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.book_id_counter = self.get_max_book_id() + 1

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                year TEXT,
                available BOOLEAN
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Borrowers (
                borrower_id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS BorrowedBooks (
                borrower_id INTEGER,
                book_id INTEGER,
                FOREIGN KEY(borrower_id) REFERENCES Borrowers(borrower_id),
                FOREIGN KEY(book_id) REFERENCES Books(book_id)
            )
        ''')

        self.conn.commit()

    def get_max_book_id(self):
        self.cursor.execute("SELECT MAX(book_id) FROM Books")
        result = self.cursor.fetchone()[0]
        return result if result is not None else 0

    def add_book(self, title, author, year):
        self.cursor.execute('INSERT INTO Books (title, author, year, available) VALUES (?, ?, ?, ?)', (title, author, year, True))
        self.conn.commit()
        print(f"\n'{title}' by {author} added to the library.")

    def remove_book(self, book_id):
        self.cursor.execute('DELETE FROM Books WHERE book_id = ?', (book_id,))
        self.conn.commit()
        print(f"Book with ID {book_id} removed from the library.")

    def add_borrower(self, borrower):
        self.cursor.execute('INSERT INTO Borrowers (borrower_id, name) VALUES (?, ?)', (borrower.borrower_id, borrower.name))
        self.conn.commit()

    def remove_borrower(self, borrower_id):
        self.cursor.execute('DELETE FROM Borrowers WHERE borrower_id = ?', (borrower_id,))
        self.conn.commit()

    def borrow_book(self, book_id, borrower_name):
        borrower_id = self.get_borrower_id(borrower_name)
        if borrower_id is not None:
            self.cursor.execute('INSERT INTO BorrowedBooks (borrower_id, book_id) VALUES (?, ?)', (borrower_id, book_id))
            self.cursor.execute('UPDATE Books SET available = ? WHERE book_id = ?', (False, book_id))
            self.conn.commit()
            print(f"\nBook with ID {book_id} borrowed by {borrower_name}.")
        else:
            print(f"Borrower {borrower_name} not found.")

    def return_book(self, book_id, borrower_name):
        borrower_id = self.get_borrower_id(borrower_name)
        if borrower_id is not None:
            self.cursor.execute('DELETE FROM BorrowedBooks WHERE borrower_id = ? AND book_id = ?', (borrower_id, book_id))
            self.cursor.execute('UPDATE Books SET available = ? WHERE book_id = ?', (True, book_id))
            self.conn.commit()
            print(f"\nBook with ID {book_id} returned by {borrower_name}.")
        else:
            print(f"Borrower {borrower_name} not found.")

    def get_borrower_id(self, borrower_name):
        self.cursor.execute('SELECT borrower_id FROM Borrowers WHERE LOWER(name) = LOWER(?)', (borrower_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def search_books(self, criteria):
        self.cursor.execute('SELECT * FROM Books WHERE title LIKE ? OR author LIKE ?', ('%' + criteria + '%', '%' + criteria + '%'))
        books = self.cursor.fetchall()
        if books:
            print("\nSearch Results:")
            for book in books:
                print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Year: {book[3]}, Available: {'Yes' if book[4] else 'No'}")
        else:
            print("No books found matching the criteria.")

    def search_borrowed_books(self, borrower_name):
        borrower_id = self.get_borrower_id(borrower_name)
        if borrower_id is not None:
            self.cursor.execute('''
                SELECT Books.title, Books.author
                FROM BorrowedBooks
                INNER JOIN Books ON BorrowedBooks.book_id = Books.book_id
                WHERE BorrowedBooks.borrower_id = ?
            ''', (borrower_id,))
            borrowed_books = self.cursor.fetchall()
            if borrowed_books:
                print(f"\nBooks borrowed by {borrower_name}:")
                for book in borrowed_books:
                    print(f"Title: {book[0]}, Author: {book[1]}")
            else:
                print(f"No books borrowed by {borrower_name}.")
        else:
            print(f"Borrower {borrower_name} not found.")

    def show_all_books(self):
        self.cursor.execute('SELECT * FROM Books')
        books = self.cursor.fetchall()
        if books:
            print("\nAll Books:")
            for book in books:
                print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Year: {book[3]}, Available: {'Yes' if book[4] else 'No'}")
        else:
            print("No books available in the library.")

    def export_to_csv(self):
        with open('books.csv', 'w', newline='') as books_file:
            books_writer = csv.writer(books_file)
            books_writer.writerow(['ID', 'Title', 'Author', 'Year', 'Available'])
            self.cursor.execute('SELECT * FROM Books')
            books = self.cursor.fetchall()
            for book in books:
                books_writer.writerow(book)

        with open('borrowers.csv', 'w', newline='') as borrowers_file:
            borrowers_writer = csv.writer(borrowers_file)
            borrowers_writer.writerow(['ID', 'Name'])
            self.cursor.execute('SELECT * FROM Borrowers')
            borrowers = self.cursor.fetchall()
            for borrower in borrowers:
                borrowers_writer.writerow(borrower)

        self.export_borrowed_books_to_csv()

    def export_borrowed_books_to_csv(self):
        with open('borrowedbooks.csv', 'w', newline='') as borrowed_books_file:
            borrowed_books_writer = csv.writer(borrowed_books_file)
            borrowed_books_writer.writerow(['Borrower ID', 'Book ID'])
            self.cursor.execute('SELECT * FROM BorrowedBooks')
            borrowed_books = self.cursor.fetchall()
            for borrowed_book in borrowed_books:
                borrowed_books_writer.writerow(borrowed_book)

# Function to interact with the library
def main():
    library = Library()
    print("Welcome to our library")

    while True:
        print("\nWhat do you want to do?")
        print("1: Show all books")
        print("2: Search books")
        print("3: Borrow a book")
        print("4: Return a book")
        print("5: Add a book")
        print("6: Remove a book")
        print("7: Add a borrower")
        print("8: Remove a borrower")
        print("9: Search borrowed books")
        print("10: Export data to CSV")
        print("11: Quit")

        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                library.show_all_books()
            elif choice == 2:
                criteria = input("Enter title or author to search: ")
                library.search_books(criteria)
            elif choice == 3:
                book_id = int(input("Enter the ID of the book you want to borrow: "))
                borrower_name = input("Enter your name: ")
                library.borrow_book(book_id, borrower_name)
            elif choice == 4:
                book_id = int(input("Enter the ID of the book you want to return: "))
                borrower_name = input("Enter your name: ")
                library.return_book(book_id, borrower_name)
            elif choice == 5:
                title = input("Enter the title of the book: ")
                author = input("Enter the author of the book: ")
                year = input("Enter the year of publication: ")
                library.add_book(title, author, year)
            elif choice == 6:
                book_id = int(input("Enter the ID of the book to remove: "))
                library.remove_book(book_id)
            elif choice == 7:
                name = input("Enter the name of the borrower: ")
                borrower_id = int(input("Enter the ID of the borrower: "))
                library.add_borrower(Borrower(name, borrower_id))
            elif choice == 8:
                borrower_id = int(input("Enter the ID of the borrower to remove: "))
                library.remove_borrower(borrower_id)
            elif choice == 9:
                borrower_name = input("Enter the name of the borrower to search: ")
                library.search_borrowed_books(borrower_name)
            elif choice == 10:
                library.export_to_csv()
            elif choice == 11:
                print("Thank you for using our library!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 11.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()
