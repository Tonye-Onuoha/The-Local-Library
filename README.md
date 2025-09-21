# 📚 Local Library

The **Local Library** is a web application built with the **Django** framework.
It allows users to create accounts, borrow or reserve books, and return them within a specific time period.

---

## 📖 Project Overview

-   Users can **sign up** and gain access to the library.
-   Members can **view, borrow, reserve, and return books**.
-   **Librarians (superusers/admins)** have extended permissions such as renewing books and viewing all borrowed books.

---

## 🔑 Features & Rules

1. ✅ **View & Review**

    - Members can view and write reviews for all books.
    - They also have access to the list of authors, genres, and available book copies.

2. 📚 **Borrowing Rules**

    - Members can borrow up to **3 books at a time**.
    - If a member has **overdue books**, no new books can be borrowed or reserved until all overdue books are returned.
    - A member **cannot borrow another copy of the same book** already borrowed.

3. 📖 **Reservation Rules**

    - A member can reserve **at most 1 book copy**.
    - A member cannot reserve a copy of a book they have already borrowed.

4. 🔄 **Returning Rules**

    - Members can return their borrowed books **anytime**, even before the due date.

5. 👤 **Access Control**
    - Members can only view their **own borrowed/reserved books**.
    - **Librarians (admins)** can:
        - Renew books
        - View all borrowed books

---

## 🛠️ Technologies

-   [Python](https://www.python.org/) – Programming language
-   [Django](https://www.djangoproject.com/) – Web framework

---

## 👥 User Roles

-   **Members** – Can view, borrow, reserve, and return books (with constraints).
-   **Librarians/Admins** – Have full control, including renewing and viewing all borrowed books.

---
