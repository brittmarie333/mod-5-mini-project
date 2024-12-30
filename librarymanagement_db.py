

import mysql.connector
from mysql.connector import Error

# Connect to MySQL database
def create_connection():
    try:
        db = mysql.connector.connect(
            host="localhost", 
            user="root",      
            password="dougfunny",       
            database="library_management_db"

        )
        print("Database connection successful!")  # To confirm connection
        return db  # Return the db connection
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None  # Return None if connection fails

class Book:
    def __init__(self, title, author_id, publication_date, availability=True):
        self.title = title
        self.author_id = author_id
        self.publication_date = publication_date
        self.availability = availability

    def add_to_db(self):
        db = create_connection()
        if not db:
            print("Failed to connect to the database.")
            return

        cursor = db.cursor()  # Create cursor after confirming connection
        query = "INSERT INTO books (title, author_id, publication_date, availability) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (self.title, self.author_id, self.publication_date, self.availability))
        db.commit()  # Commit the changes to the database
        print(f"Book '{self.title}' added to the database.")  # Feedback to user
        cursor.close()  # Close cursor after work is done
        db.close()  # Close connection after work is done

    
    def search_books(title=None, author_name=None):
        """Search for books by title or author."""
        db = create_connection()
        if not db:
            print("Failed to connect to the database.")
            return []

        cursor = db.cursor(dictionary=True)

        if not title and not author_name:
            raise ValueError("Please provide either a title or an author name to search.")

        if title and author_name:
            query = "SELECT b.* FROM books b JOIN authors a ON b.author_id = a.id WHERE b.title LIKE %s AND a.name LIKE %s"
            cursor.execute(query, ('%' + title + '%', '%' + author_name + '%'))
        elif title:
            query = "SELECT * FROM books WHERE title LIKE %s"
            cursor.execute(query, ('%' + title + '%',))
        elif author_name:
            query = "SELECT b.* FROM books b JOIN authors a ON b.author_id = a.id WHERE a.name LIKE %s"
            cursor.execute(query, ('%' + author_name + '%',))

        books = cursor.fetchall()
        cursor.close()
        db.close()
        return books

class User:
    def __init__(self, name, library_id):
        self.name = name
        self.library_id = library_id

    def add_to_db(self):
        """Add a new user to the database."""
        db = create_connection()
        if not db:
            print("Failed to connect to the database.")
            return

        cursor = db.cursor()
        query = "INSERT INTO users (name, library_id) VALUES (%s, %s)"
        cursor.execute(query, (self.name, self.library_id))
        db.commit()
        print(f"User '{self.name}' added to the database.")
        cursor.close()
        db.close()


    def get_user_details(library_id):
        db = create_connection()
        if not db:
            print("Failed to connect to the database.")
            return None

        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE library_id = %s"
        cursor.execute(query, (library_id,))
        user = cursor.fetchone()
        cursor.close()
        db.close()
        return user

def borrow_book():
    user_id = int(input("Enter your user ID: "))
    book_id = int(input("Enter book ID: "))
    borrow_date = input("Enter borrow date (YYYYMM): ")

    db = create_connection()
    if not db:
        print("Failed to connect to the database.")
        return
    cursor = db.cursor()
    cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if not user:
        print("User not found.")
        cursor.close()
        db.close()
        return
    
    cursor.execute("SELECT id, availability FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    if not book:
        print("Book not found.")
        cursor.close()
        db.close()
        return

    if not book[1]: 
        print("Sorry, this book is already borrowed.")
        cursor.close()
        db.close()
        return

    query = "INSERT INTO borrowed_books (user_id, book_id, borrow_date) VALUES (%s, %s, %s)"
    cursor.execute(query, (user_id, book_id, borrow_date))
    cursor.execute("UPDATE books SET availability = False WHERE id = %s", (book_id,))

    db.commit()  
    cursor.close()
    db.close()
    print("Book borrowed successfully! Please return on time.")

def return_book():
    user_id = int(input("Enter your user ID: "))
    book_id = int(input("Enter book ID: "))
    return_date = input("Enter return date (YYYY-MM-DD): ")
    db = create_connection()
    if not db:
        print("Failed to connect to the database.")
        return
    
    cursor = db.cursor()
    query = "UPDATE borrowed_books SET return_date = %s WHERE user_id = %s AND book_id = %s"
    cursor.execute(query, (return_date, user_id, book_id))
    cursor.execute("UPDATE books SET availability = True WHERE id = %s", (book_id,))
    db.commit()  # Commit the update
    cursor.close()
    db.close()
    print("Book successfully returned.")

class Author:
    def __init__(self, name):
        self.name = name

    def add_to_db(self):
        db = create_connection()
        if not db:
            print("Failed to connect to the database.")
            return

        cursor = db.cursor()
        query = "INSERT INTO authors (name) VALUES (%s)"
        cursor.execute(query, (self.name,))
        db.commit()  # Commit after the insert
        print(f"Author '{self.name}' added to the database.")
        cursor.close()
        db.close()

    @staticmethod
    def search_authors(name=None):
        db = create_connection()
        if not db:
            print("Failed to connect to the database.")
            return []

        cursor = db.cursor(dictionary=True)

        if not name:
            raise ValueError("Please provide an author name to search.")

        query = "SELECT * FROM authors WHERE name LIKE %s"
        cursor.execute(query, ('%' + name + '%',))
        authors = cursor.fetchall()
        cursor.close()
        db.close()
        return authors

def author_operations():
    while True:
        print("\nAuthor Operations:")
        print("1. Add a new author")
        print("2. Search for an author")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter author name: ")
            author = Author(name)
            author.add_to_db()
            print("Author added successfully.")
        elif choice == '2':
            name = input("Enter author name to search: ")
            authors = Author.search_authors(name=name)
            if authors:
                for author in authors:
                    print(f"ID: {author['id']}, Name: {author['name']}")
            else:
                print("No authors found with that name.")
        elif choice == '3':
            break
        else:
            print("Invalid choice! Please try again.")

def main_menu():
    while True:
        print("\nWelcome to the Library Management System")
        print("1. Book Operations")
        print("2. User Operations")
        print("3. Author Operations")
        print("4. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            book_operations()
        elif choice == '2':
            user_operations()
        elif choice == '3':
            author_operations()
        elif choice == '4':
            print("Exiting the system...")
            break
        else:
            print("Invalid choice! Please try again.")

def book_operations():
    while True:
        print("\nBook Operations:")
        print("1. Add a new book")
        print("2. Borrow a book")
        print("3. Return a book")
        print("4. Search for a book")
        print("5. Display all books")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter book title: ")
            author_id = int(input("Enter author ID: "))
            publication_date = input("Enter publication date (YYYYMM): ")
            book = Book(title, author_id, publication_date)
            book.add_to_db()
            print("Book added successfully.")
        elif choice == '2':
            borrow_book()
        elif choice == '3':
            return_book()
        elif choice == '4':
            title = input("Enter book title to search: ")
            books = Book.search_books(title=title)
            for book in books:
                print(book)
        elif choice == '5':
            db = create_connection()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM books")
            books = cursor.fetchall()
            for book in books:
                print(book)
            cursor.close()
            db.close()
        elif choice == '6':
            break
        else:
            print("Invalid choice! Please try again.")

def user_operations():
    while True:
        print("\nUser Operations:")
        print("1. Add a new user")
        print("2. View user details")
        print("3. Display all users")
        print("4. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter user name: ")
            library_id = input("Enter library ID: ")
            user = User(name, library_id)
            user.add_to_db()
            print("User added successfully.")
        elif choice == '2':
            library_id = input("Enter user library ID: ")
            user = User.get_user_details(library_id)
            print(user)
        elif choice == '3':
            db = create_connection()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            for user in users:
                print(user)
            cursor.close()
            db.close()
        elif choice == '4':
            break
        else:
            print("Invalid choice! Please try again.")

# Run the program
if __name__ == "__main__":
    main_menu()
