import csv
import os
from datetime import timedelta

class User:
    """
        Initialize a User object.

        Args:
        - user_name (str): The name of the user.
        - user_type (str): The type of the user (either 'user' or 'admin').
        - user_phone (str): The phone number of the user.
        - user_email (str): The email address of the user.
        - password (str): The password for user authentication.
        """
    def __init__(self, user_name, user_type, user_phone, user_email, password):
        self.user_name = user_name
        self.user_type = user_type
        self.user_phone = user_phone
        self.user_email = user_email
        self.password = password

    def register(self):
        """
        Register the user by adding user details to the 'users.csv' file.
        """
        with open('users.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.user_name, self.user_type, self.user_phone, self.user_email, self.password])
        print(f"User {self.user_name} registered successfully.")

    def login(self, entered_password):
        """
        Log in the user by verifying the entered password.

        Args:
        - entered_password (str): The password entered by the user for login.
        """
        if entered_password == self.password:
            print(f"User {self.user_name} logged in.")
        else:
            print("Incorrect password. Login failed.")

    def search(self, search_query, library):
        """
        Search for books in the library based on the provided query.

        Args:
        - search_query (str): The query string to search for in book titles or authors.
        - library (Library): The Library object representing the library system.
        """
        matching_books = library.search_books(search_query)
        if matching_books:
            print("Matching Books:")
            for book in matching_books:
                print(f"ISBN: {book.book_id}, Title: {book.book_title}, Availability: {book.availability}")
        else:
            print("No matching books found.")

    def reservation(self, book_id, library):
        """
        Reserve a book in the library.

        Args:
        - book_id (str): The ISBN of the book to be reserved.
        - library (Library): The Library object representing the library system.
        """
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

    def renew_book(self, book_id, library):
        """
        Renew a reserved book in the library.

        Args:
        - book_id (str): The ISBN of the book to be renewed.
        - library (Library): The Library object representing the library system.
        """
        book_to_renew = library.find_book_by_id(book_id)

        if book_to_renew:
            if book_to_renew.reserved and not book_to_renew.availability:
                book_to_renew.due_return += timedelta(days=14)
                library.save_books()

                print(f"Book '{book_to_renew.book_title}' renewed successfully. New due date: {book_to_renew.due_return}")
            else:
                print("Book cannot be renewed. Check availability and reservation status.")
        else:
            print("Book not found.")


class Admin(User):
    def __init__(self, user_name, user_type, user_phone, user_email, password):
        """
        Initialize an Admin object, inheriting from User.

        Args:
        - user_name (str): The name of the admin.
        - user_type (str): The type of the admin (always 'admin').
        - user_phone (str): The phone number of the admin.
        - user_email (str): The email address of the admin.
        - password (str): The password for admin authentication.
        """
        super().__init__(user_name, "admin", user_phone, user_email, password)

    def register(self):
        """
        Register the admin by adding admin details to the 'users.csv' file.
        """
        with open('users.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.user_name, "admin", self.user_phone, self.user_email, self.password])
        print(f"Admin {self.user_name} registered successfully.")

    def add_book(self, library):
        """
        Add a book to the library's collection.

        Args:
        - library (Library): The Library object representing the library system.
        """
        ISBN = input("Enter the book's ISBN: ")
        title = input("Enter the book's title: ")
        author = input("Enter the book's author: ")

        new_book = Book(ISBN, title, author)
        library.add_book(new_book)

        print(f"Book {title} added successfully.")

    def delete_book(self, library):
        """
        Delete a book from the library's collection.

        Args:
        - library (Library): The Library object representing the library system.
        """
        book_id = input("Enter the book ISBN to delete: ")
        if any(book.book_id == book_id for book in library.books):
            updated_books = [book for book in library.books if book.book_id != book_id]
            library.books = updated_books
            library.save_books()
            print(f"Book with ISBN {book_id} deleted successfully.")
        else:
            print(f"Book with ISBN {book_id} not found.")

    def view_users(self, library):
        """
        View information about all users registered in the library.

        Args:
        - library (Library): The Library object representing the library system.
        """
        print("Viewing user information:")
        for user in library.users:
            print(f"User Name: {user.user_name}, User Type: {user.user_type}, Phone: {user.user_phone}, Email: {user.user_email}")

class Book:
    def __init__(self, book_id, book_title, book_author, availability=None, reserved=False, due_return=False):
        """
        Initialize a Book object.

        Args:
        - book_id (str): The ISBN of the book.
        - book_title (str): The title of the book.
        - book_author (str): The author of the book.
        - availability (bool): The availability status of the book (default is True).
        - reserved (bool): The reservation status of the book (default is False).
        - due_return (datetime): The due return date of the book (default is None).
        """
        self.book_id = book_id
        self.book_title = book_title
        self.book_author = book_author
        self.availability = availability
        self.reserved = reserved
        self.due_return = due_return

    def availability_status(self):
        """
        Get the availability status of the book.

        Returns:
        - str: The availability status ('Available' or 'Not Available').
        """
        return "Available" if self.availability and not self.reserved else "Not Available"

class System:
    """
        Represents the library system.

        Attributes:
        - due_return (str): The due return date.
        - student_id (str): The ID of the student.
        """
    
    def __init__(self, due_return, student_id):
        """
        Initializes a new System object.

        Parameters:
        - due_return (str): The due return date.
        - student_id (str): The ID of the student.
        """
        self.due_return = due_return
        self.student_id = student_id

    def default(self):
        """Defines the default system behavior."""
        print("Default system behavior...")

class Student:
    """
    Represents a student in the library system.

    Attributes:
    - student_id (str): The ID of the student.
    """

    def __init__(self, student_id):
        """
        Initializes a new Student object.

        Parameters:
        - student_id (str): The ID of the student.
        """
        self.student_id = student_id

    def return_book(self):
        """Handles the process of returning a book."""
        print("Returning a book...")

    def pay_fine(self):
        """Handles the process of paying fines."""
        print("Paying fines...")

class Clerk:
    """
    Represents a clerk in the library system.

    Attributes:
    - clerk_id (str): The ID of the clerk.
    """

    def __init__(self, clerk_id):
        """
        Initializes a new Clerk object.

        Parameters:
        - clerk_id (str): The ID of the clerk.
        """
        self.clerk_id = clerk_id

    def sort_book(self):
        """Handles the process of sorting books."""
        print("Sorting books...")

    def update_book(self):
        """Handles the process of updating book information."""
        print("Updating book information...")

    def issue_book(self):
        """Handles the process of issuing a book."""
        print("Issuing a book...")

    def calc_fine(self):
        """Handles the process of calculating fines."""
        print("Calculating fines...")

class PayFine:
    """
    Represents the process of paying fines.

    Attributes:
    - pay_id (str): The ID of the payment.
    - pay_description (str): The description of the payment.
    - student_id (str): The ID of the student making the payment.
    """

    def __init__(self, pay_id, pay_description, student_id):
        """
        Initializes a new PayFine object.

        Parameters:
        - pay_id (str): The ID of the payment.
        - pay_description (str): The description of the payment.
        - student_id (str): The ID of the student making the payment.
        """
        self.pay_id = pay_id
        self.pay_description = pay_description
        self.student_id = student_id

    def create_pay(self):
        """Handles the process of creating a payment record."""
        print("Creating a payment record...")

    def payment_type(self):
        """Handles the process of specifying payment type."""
        print("Specifying payment type...")

    def confirm_pay(self):
        """Handles the process of confirming payment."""
        print("Confirming payment...")

class RenewBook:
    """
    Represents the process of renewing a book.

    Attributes:
    - book_id (str): The ID of the book to renew.
    - student_id (str): The ID of the student renewing the book.
    """
    def __init__(self, book_id, student_id):
        """
        Initializes a new RenewBook object.

        Parameters:
        - book_id (str): The ID of the book to renew.
        - student_id (str): The ID of the student renewing the book.
        """
        self.book_id = book_id
        self.student_id = student_id

    def issue(self):
        """Handles the process of renewing a book."""
        print("Renewing a book...")

class CalculateFine:
    """
    Represents the process of calculating fines.

    Attributes:
    - fine_id (str): The ID of the fine.
    - student_id (str): The ID of the student with fines.
    - total_balance (float): The total fine balance.
    """

    def __init__(self, fine_id, student_id, total_balance):
        """
        Initializes a new CalculateFine object.

        Parameters:
        - fine_id (str): The ID of the fine.
        - student_id (str): The ID of the student with fines.
        - total_balance (float): The total fine balance.
        """
        self.fine_id = fine_id
        self.student_id = student_id
        self.total_balance = total_balance

    def method(self):
        """Handles the process of calculating fines."""
        print("Calculating fines...")

class SearchBook:
    """
    Represents the process of searching for a book.

    Attributes:
    - book_id (str): The ID of the book to search.
    - book_title (str): The title of the book to search.
    """

    def __init__(self, book_id, book_title):
        """
        Initializes a new SearchBook object.

        Parameters:
        - book_id (str): The ID of the book to search.
        - book_title (str): The title of the book to search.
        """
        self.book_id = book_id
        self.book_title = book_title

    def availability_status(self):
        """Handles the process of checking book availability status."""
        print("Checking book availability status...")

class ReserveBook:
    def __init__(self, book_id, student_id):
        """
        Represents the process of reserving a book.

        Attributes:
        - book_id (str): The ID of the book to reserve.
        - student_id (str): The ID of the student reserving the book.
        """
        self.book_id = book_id
        self.student_id = student_id

    def reserved(self):
        print("Reserving a book...")

class IssueBook:
    """
    Represents the process of issuing a book.

    Attributes:
    - book_id (str): The ID of the book to issue.
    - student_id (str): The ID of the student issuing the book.
    """

    def __init__(self, book_id, student_id):
        """
        Initializes a new IssueBook object.

        Parameters:
        - book_id (str): The ID of the book to issue.
        - student_id (str): The ID of the student issuing the book.
        """
        self.book_id = book_id
        self.student_id = student_id

    def issue(self):
        """Handles the process of issuing a book."""
        print("Issuing a book...")

def load_books_from_file():
    """
    Loads books from the 'books.csv' file.

    Returns:
    - List[Book]: List of Book objects.
    """
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
    """
    Loads users from the 'users.csv' file.

    Returns:
    - List[User]: List of User objects.
    """
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
    """
    Displays the library system menu based on the user type.

    Parameters:
    - user (User): The current user of the system.
    - library (Library): The library instance.
    """
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
    """
    Represents a library.

    Attributes:
    - name (str): The name of the library.
    - book_file (str): The file path for book data.
    - user_file (str): The file path for user data.
    """

    def __init__(self, name, book_file, user_file):
        """
        Initializes a new Library object.

        Parameters:
        - name (str): The name of the library.
        - book_file (str): The file path for book data.
        - user_file (str): The file path for user data.
        """
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
                books = [Book(row['book_id'], row['book_title'], row['availability'], row['reserved'], row['due_return']) for row in reader]
            return books
        except FileNotFoundError:
            return []
        
    def find_book_by_id(self, book_id):
        """
        Finds a book by its ID.

        Parameters:
        - book_id (str): The ID of the book to find.

        Returns:
        - Book or None: The Book object if found, otherwise None.
        """
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None

    
        
    def load_users(self):
        """
        Loads users from the CSV file.

        Returns:
        - List[User]: List of User objects.
        """
        try:
            with open(self.user_file, 'r') as file:
                reader = csv.DictReader(file)
                users = [User(row['user_name'], row['user_type'], row['user_phone'], row['user_email'], row['password']) for row in reader]
            return users
        except FileNotFoundError:
            return []
        
    def add_book(self, book):
        """
        Adds a book to the library.

        Parameters:
        - book (Book): The Book object to add.
        """
        self.books.append(book)
        self.save_books()

    def add_member(self, member):
        """
        Adds a member to the library.

        Parameters:
        - member (User): The User object to add.
        """
        self.members.append(member)
        self.save_members()

    def save_books(self):
        """
        Saves books to the CSV file.
        """
        try:
            with open(self.book_file, 'w', newline='') as file:
                fieldnames = ['book_id', 'book_title', 'availability', 'reserved', 'due_return']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for book in self.books:
                    writer.writerow({
                        'book_id': book.book_id,
                        'book_title': book.book_title,
                        'availability': book.availability,
                        'reserved': book.reserved,
                        'due_return': book.due_return.strftime('%Y-%m-%d') if book.due_return else ''
                    })
        except Exception as e:
            print(f"Error saving books: {e}")

    def search_books(self, search_query):
        """
        Searches for books based on a search query.

        Parameters:
        - search_query (str): The search query.

        Returns:
        - List[Book]: List of matching Book objects.
        """
        matching_books = [book for book in self.books if search_query.lower() in book.book_title.lower()]
        return matching_books
    
        
def main():
    """
    Main function to run the library system.
    """
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
                book_id_to_reserve = input("Enter the book ISBN to reserve: ")
                user.reservation(book_id_to_reserve, library)
            else:
                print("Please register first.")
        elif choice == '5':
            if user:
                book_id = input("Enter the book ISBN you want to renew: ")
                user.renew_book(book_id, library)
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