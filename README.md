
# Library Management System

## Overview
The Library Management System is a simple Python program that helps manage books and members in a library. It allows users to add and remove books, add and delete members, check out and return books, and display information about available books and library members.

## Features
- **Book Management:**
  - Add a new book to the library.
  - Delete a book by ISBN.
  - Display a list of available books.

- **Member Management:**
  - Add a new member to the library.
  - Delete a member by ID.
  - Display a list of library members.

- **Book Checkout and Return:**
  - Check out a book to a library member.
  - Return a book to the library.

- **Data Persistence:**
  - Data (books and members) is stored in CSV files to ensure persistence between program runs.

## Requirements
- Python 3.x

## Getting Started
1. Clone the repository to your local machine.
   ```bash
   git clone https://github.com/akinsiraifedayo/library-management-system.git
   cd library-management-system
   ```

2. Run the program.
   ```bash
   python main.py
   ```

3. Follow the on-screen menu to perform various operations.

## Menu Options
- **Display Available Books (1):**
  Displays a list of available books in the library.

- **Display Library Members (2):**
  Displays a list of library members.

- **Check Out Book (3):**
  Allows a member to check out a book by providing their ID and the book's ISBN.

- **Return Book (4):**
  Allows a member to return a checked-out book by providing their ID and the book's ISBN.

- **Delete Book (5):**
  Deletes a book from the library by providing its ISBN.

- **Delete Member (6):**
  Deletes a member from the library by providing their ID.

- **Exit (7):**
  Exits the program.

- **Add Member (8):**
  Adds a new member to the library by providing their name and ID.

- **Add Book (9):**
  Adds a new book to the library by providing its title, author, and ISBN.

```