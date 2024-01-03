import csv
import os
from datetime import datetime, timedelta
from typing import List

class User:
    def __init__(self, user_name, user_type, user_phone, user_email, password):
        self.user_name = user_name
        self.user_type = user_type
        self.user_phone = user_phone
        self.user_email = user_email
        self.password = password

    def register(self):
        with open('users.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.user_name, self.user_type, self.user_phone, self.user_email, self.password])
        print(f"User {self.user_name} registered successfully.")

    def login(self, entered_password):
        if entered_password == self.password:
            print(f"User {self.user_name} logged in.")
        else:
            print("Incorrect password. Login failed.")

    def search(self, search_query, library):
        matching_books = library.search_books(search_query)
        if matching_books:
            print("Matching Books:")
            for book in matching_books:
                print(f"ID: {book.book_id}, Title: {book.book_title}, Availability: {book.availability}")
        else:
            print("No matching books found.")

    def reservation(self, book_id, library):
        book_to_reserve = library.find_book_by_id(book_id)

        if book_to_reserve:
            if book_to_reserve.availability and not book_to_reserve.reserved:
                book_to_reserve.reserved = True
                print(f"Book '{book_to_reserve.book_title}' reserved successfully.")
            elif not book_to_reserve.availability:
                print("Book is not available for reservation.")
            elif book_to_reserve.reserved:
                print("Book is already reserved.")
        else:
            print("Book not found.")

    def renew(self):
        print("Renewing a reserved book.")


class Admin(User):
    def __init__(self, user_name, user_type, user_phone, user_email, password):
        super().__init__(user_name, "admin", user_phone, user_email, password)

    def register(self):
        with open('users.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.user_name, "admin", self.user_phone, self.user_email, self.password])
        print(f"Admin {self.user_name} registered successfully.")

    def add_book(self, library):
        title = input("Enter the book's title: ")
        author = input("Enter the book's author: ")
        ISBN = input("Enter the book's ISBN: ")

        new_book = Book(title, author, ISBN)
        library.add_book(new_book)

        print(f"Book {title} added successfully.")

    def delete_book(self, library):
        book_id = input("Enter the book ID to delete: ")
        if any(book.book_id == book_id for book in library.books):
            updated_books = [book for book in library.books if book.book_id != book_id]
            library.books = updated_books
            library.save_books()
            print(f"Book with ID {book_id} deleted successfully.")
        else:
            print(f"Book with ID {book_id} not found.")

    def view_users(self, library):
        print("Viewing user information:")
        for user in library.users:
            print(f"User Name: {user.user_name}, User Type: {user.user_type}, Phone: {user.user_phone}, Email: {user.user_email}")

class Book:
    def __init__(self, book_id, book_title, availability, reserved):
        self.book_id = book_id
        self.book_title = book_title
        self.availability = availability
        self.reserved = reserved

    def availability_status(self):
        return "Available" if self.availability and not self.reserved else "Not Available"

class System:
    def __init__(self, due_return, student_id):
        self.due_return = due_return
        self.student_id = student_id

    def default(self):
        print("Default system behavior...")

class Student:
    def __init__(self, student_id):
        self.student_id = student_id

    def return_book(self):
        print("Returning a book...")

    def pay_fine(self):
        print("Paying fines...")

class Clerk:
    def __init__(self, clerk_id):
        self.clerk_id = clerk_id

    def sort_book(self):
        print("Sorting books...")

    def update_book(self):
        print("Updating book information...")

    def issue_book(self):
        print("Issuing a book...")

    def calc_fine(self):
        print("Calculating fines...")

class PayFine:
    def __init__(self, pay_id, pay_description, student_id):
        self.pay_id = pay_id
        self.pay_description = pay_description
        self.student_id = student_id

    def create_pay(self):
        print("Creating a payment record...")

    def payment_type(self):
        print("Specifying payment type...")

    def confirm_pay(self):
        print("Confirming payment...")

class RenewBook:
    def __init__(self, book_id, student_id):
        self.book_id = book_id
        self.student_id = student_id

    def issue(self):
        print("Renewing a book...")

class CalculateFine:
    def __init__(self, fine_id, student_id, total_balance):
        self.fine_id = fine_id
        self.student_id = student_id
        self.total_balance = total_balance

    def method(self):
        print("Calculating fines...")

class SearchBook:
    def __init__(self, book_id, book_title):
        self.book_id = book_id
        self.book_title = book_title

    def availability_status(self):
        print("Checking book availability status...")

class ReserveBook:
    def __init__(self, book_id, student_id):
        self.book_id = book_id
        self.student_id = student_id

    def reserved(self):
        print("Reserving a book...")

class IssueBook:
    def __init__(self, book_id, student_id):
        self.book_id = book_id
        self.student_id = student_id

    def issue(self):
        print("Issuing a book...")

def load_books_from_file():
    books = []
    try:
        with open('books.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                books.append(Book(*row))
    except FileNotFoundError:
        pass
    return books

def load_users_from_file():
    users = []
    try:
        with open('users.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == 'user':
                    users.append(User(*row))
                elif row[1] == 'admin':
                    users.append(Admin(*row))
    except FileNotFoundError:
        pass
    return users


def display_menu(user, library):
    print("\nLibrary System Menu:")
    if not user:
        print("1. Register User")
        print("2. Login User")
    
    if isinstance(user, Admin) or isinstance(user, User):
        print("3. Search Books")
        print("4. Reserve Book")
        print("5. Renew Book")

    if isinstance(user, Admin):
        print("6. Add Book")
        print("7. Delete Book")
        print("8. View Users")

    print("9. Exit")

class Library:
    def __init__(self, name, book_file, user_file):
        self.name = name
        self.book_file = os.path.join(os.getcwd(), book_file)
        self.user_file = os.path.join(os.getcwd(), user_file)
        self.books = self.load_books()
        self.users = self.load_users()

    

    def load_books(self):
        """
        Loads books from the CSV file.

        Returns:
        - List[Book]: List of Book objects.
        """
        try:
            with open(self.book_file, 'r') as file:
                reader = csv.DictReader(file)
                books = [Book(row['book_id'], row['book_title'], row['availability'], row['reserved']) for row in reader]
            return books
        except FileNotFoundError:
            return []
        
    def find_book_by_id(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None

    
        
    def load_users(self):
        try:
            with open(self.user_file, 'r') as file:
                reader = csv.DictReader(file)
                users = [User(row['user_name'], row['user_type'], row['user_phone'], row['user_email'], row['password']) for row in reader]
            return users
        except FileNotFoundError:
            return []
        
    def add_book(self, book):
        self.books.append(book)
        self.save_books()

    def add_member(self, member):
        self.members.append(member)
        self.save_members()

    def save_books(self):
        with open(self.book_file, 'w', newline='') as file:
            writer = csv.writer(file)
            for book in self.books:
                writer.writerow([book.book_id, book.book_title, book.availability, book.reserved])

    def search_books(self, search_query):
        matching_books = [book for book in self.books if search_query.lower() in book.book_title.lower()]
        return matching_books
    
        
def main():
    library = Library("My Library", "books.csv", "users.csv")
    users = load_users_from_file()
    books = load_books_from_file()
    user = None 

    while True:
        display_menu(user, library)
        choice = input("Enter your choice (1-9): ")

        if choice == '1':
            user_name = input("Enter your name: ")
            user_type = input("Enter your user type (user/admin): ")
            user_phone = input("Enter your phone number: ")
            user_email = input("Enter your email: ")
            password = input("Enter your password: ")
            
            if user_type.lower() == 'user':
                user = User(user_name, user_type, user_phone, user_email, password)

            elif user_type.lower() == 'admin':
                user = Admin(user_name, user_type, user_phone, user_email, password)

            user.register()
            users.append(user)
        elif choice == '2':
            user_name = input("Enter your name: ")
            entered_password = input("Enter your password: ")

            # Find the user in the list of registered users
            matching_users = [u for u in users if u.user_name == user_name]

            if matching_users:
                user = matching_users[0]
                user.login(entered_password)
            else:
                print("User not found. Please register first.")
        elif choice == '3':
            if user:
                search_query = input("Enter the book title or author: ")
                user.search(search_query, library)
            else:
                print("Please register first.")
        elif choice == '4':
            if user:
                book_id_to_reserve = input("Enter the book ID to reserve: ")
                user.reservation(book_id_to_reserve, library)
            else:
                print("Please register first.")
        elif choice == '5':
            if user:
                user.renew()
            else:
                print("Please register first.")
        elif choice == '6' and isinstance(user, Admin):
            user.add_book(library)

        elif choice == '7' and isinstance(user, Admin):
            user.delete_book(library)
        elif choice == '8' and isinstance(user, Admin):
            user.view_users(library)
        elif choice == '9':
            print("Exiting program. Thank you!")
            library.save_books()
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 9.")

if __name__ == "__main__":
    main()