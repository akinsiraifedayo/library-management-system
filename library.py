import os
import csv
from datetime import datetime, timedelta

class Book:
    def __init__(self, title, author, ISBN):
        """
        Represents a Book in the library.

        Args:
        - title (str): The title of the book.
        - author (str): The author of the book.
        - ISBN (str): The ISBN (International Standard Book Number) of the book.
        """
        self.title = title
        self.author = author
        self.ISBN = ISBN
        self.checked_out_by = None
        self.due_date = None

    def display_info(self):
        """
        Displays information about the book.
        """
        print(f"Title: {self.title}, Author: {self.author}, ISBN: {self.ISBN}")

class Member:
    def __init__(self, name, member_id):
        """
        Represents a Member in the library.

        Args:
        - name (str): The name of the member.
        - member_id (int): The unique identifier for the member.
        """
        self.name = name
        self.member_id = member_id
        self.checked_out_books = []

    def check_out_book(self, book, due_date):
        """
        Checks out a book to the member.

        Args:
        - book (Book): The book to be checked out.
        - due_date (datetime): The due date for returning the book.
        """
        book.checked_out_by = self
        book.due_date = due_date
        self.checked_out_books.append(book)

    def return_book(self, book):
        """
        Returns a book that was checked out by the member.

        Args:
        - book (Book): The book to be returned.
        """
        if book in self.checked_out_books:
            book.checked_out_by = None
            book.due_date = None
            self.checked_out_books.remove(book)

class Library:
    def __init__(self, name, book_file, member_file):
        """
        Represents a Library with books and members.

        Args:
        - name (str): The name of the library.
        - book_file (str): The filename for storing book data.
        - member_file (str): The filename for storing member data.
        """
        self.name = name
        # Construct full file paths based on the current working directory
        self.book_file = os.path.join(os.getcwd(), book_file)
        self.member_file = os.path.join(os.getcwd(), member_file)
        self.books = self.load_books()
        self.members = self.load_members()

    def load_books(self):
        """
        Loads books from the CSV file.

        Returns:
        - List[Book]: List of Book objects.
        """
        try:
            with open(self.book_file, 'r') as file:
                reader = csv.DictReader(file)
                books = [Book(row['Title'], row['Author'], row['ISBN']) for row in reader]
            return books
        except FileNotFoundError:
            return []

    def load_members(self):
        """
        Loads members from the CSV file.

        Returns:
        - List[Member]: List of Member objects.
        """
        try:
            with open(self.member_file, 'r') as file:
                reader = csv.DictReader(file)
                members = [Member(row['Name'], int(row['MemberID'])) for row in reader]
            return members
        except FileNotFoundError:
            return []

    def save_books(self):
        """
        Saves books to the CSV file.
        """
        with open(self.book_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Title', 'Author', 'ISBN'])
            writer.writeheader()
            for book in self.books:
                writer.writerow({'Title': book.title, 'Author': book.author, 'ISBN': book.ISBN})

    def save_members(self):
        """
        Saves members to the CSV file.
        """
        with open(self.member_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Name', 'MemberID'])
            writer.writeheader()
            for member in self.members:
                writer.writerow({'Name': member.name, 'MemberID': member.member_id})

    def add_book(self, book):
        """
        Adds a book to the library.

        Args:
        - book (Book): The book to be added.
        """
        self.books.append(book)
        self.save_books()

    def add_member(self, member):
        """
        Adds a member to the library.

        Args:
        - member (Member): The member to be added.
        """
        self.members.append(member)
        self.save_members()

    def delete_book(self, ISBN):
        """
        Deletes a book from the library based on its ISBN.

        Args:
        - ISBN (str): The ISBN of the book to be deleted.
        """
        book = next((b for b in self.books if b.ISBN == ISBN), None)
        if book:
            self.books.remove(book)
            self.save_books()
            print(f"Book with ISBN {ISBN} deleted successfully.")
        else:
            print(f"Book with ISBN {ISBN} not found.")

    def delete_member(self, member_id):
        """
        Deletes a member from the library based on their ID.

        Args:
        - member_id (int): The ID of the member to be deleted.
        """
        member = next((m for m in self.members if m.member_id == member_id), None)
        if member:
            self.members.remove(member)
            self.save_members()
            print(f"Member with ID {member_id} deleted successfully.")
        else:
            print(f"Member with ID {member_id} not found.")

    def display_books(self):
        """
        Displays information about all available books in the library.
        """
        for book in self.books:
            book.display_info()

    def display_members(self):
        """
        Displays information about all library members.
        """
        for member in self.members:
            print(f"Member ID: {member.member_id}, Name: {member.name}")

    def check_out_book(self, member_id, ISBN):
        """
        Checks out a book to a member based on member ID and book ISBN.

        Args:
        - member_id (int): The ID of the member.
        - ISBN (str): The ISBN of the book to be checked out.
        """
        member = next((m for m in self.members if m.member_id == member_id), None)
        book = next((b for b in self.books if b.ISBN == ISBN and not b.checked_out_by), None)

        if member and book:
            due_date = datetime.now() + timedelta(days=14)  # Example: 2 weeks checkout period
            member.check_out_book(book, due_date)
            print(f"{book.title} checked out to {member.name}. Due date: {due_date}")
        elif not member:
            print(f"Member with ID {member_id} not found.")
        elif not book:
            print(f"Book with ISBN {ISBN} not available for checkout.")

    def return_book(self, member_id, ISBN):
        """
        Returns a book to the library based on member ID and book ISBN.

        Args:
        - member_id (int): The ID of the member.
        - ISBN (str): The ISBN of the book to be returned.
        """
        member = next((m for m in self.members if m.member_id == member_id), None)
        book = next((b for b in self.books if b.ISBN == ISBN and b.checked_out_by == member), None)

        if member and book:
            member.return_book(book)
            print(f"{book.title} returned by {member.name}.")
        elif not member:
            print(f"Member with ID {member_id} not found.")
        elif not book:
            print(f"Book with ISBN {ISBN} not checked out by {member.name}.")

def display_menu():
    """
    Displays the main menu of the library management system.
    """
    print("\nLibrary Management System")
    print("1. Display Available Books")
    print("2. Display Library Members")
    print("3. Check Out Book")
    print("4. Return Book")
    print("5. Delete Book")
    print("6. Delete Member")
    print("7. Exit")
    print("8. Add Member")
    print("9. Add Book")

def main():
    """
    Main function to run the library management system.
    """
    library = Library("My Library", "books.csv", "members.csv")

    while True:
        display_menu()
        choice = input("Enter your choice (1-9): ")

        if choice == '1':
            print("\nAvailable Books:")
            library.display_books()
        elif choice == '2':
            print("\nLibrary Members:")
            library.display_members()
        elif choice == '3':
            member_id = input("Enter your member ID: ")
            ISBN = input("Enter the ISBN of the book you want to check out: ")
            library.check_out_book(int(member_id), ISBN)
        elif choice == '4':
            member_id = input("Enter your member ID: ")
            ISBN = input("Enter the ISBN of the book you want to return: ")
            library.return_book(int(member_id), ISBN)
        elif choice == '5':
            ISBN = input("Enter the ISBN of the book you want to delete: ")
            library.delete_book(ISBN)
        elif choice == '6':
            member_id = input("Enter the member ID you want to delete: ")
            library.delete_member(int(member_id))
        elif choice == '7':
            print("Exiting program. Thank you!")
            break
        elif choice == '8':
            name = input("Enter the member's name: ")
            member_id = int(input("Enter the member's ID: "))
            new_member = Member(name, member_id)
            library.add_member(new_member)
            print(f"Member {name} added successfully.")
        elif choice == '9':
            title = input("Enter the book's title: ")
            author = input("Enter the book's author: ")
            ISBN = input("Enter the book's ISBN: ")
            new_book = Book(title, author, ISBN)
            library.add_book(new_book)
            print(f"Book {title} added successfully.")
        else:
            print("Invalid choice. Please enter a number between 1 and 9.")

if __name__ == "__main__":
    main()
