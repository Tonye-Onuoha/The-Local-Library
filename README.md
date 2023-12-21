# Local library
This is a repository for a personal project called the "Local Library".
The Local Library is a web application that was created using the Django web framework. It enables it's users to create accounts for access to borrow or reserve some of their favorite books for a specific period of time.
Library members are given the permission to return books upon first creating an account.
Members are allowed to view, borrow or reserve books with the following constraints:
	1. Members have full access to view and write reviews for all books in the library. They also have full access to the list of all authors, genres and copies of books available. 
	2. A member is only allowed to borrow at most 3 books for a certain period i.e a member cannot borrow more than 3 book copies from the library.
	3. If a member has a book that is overdue (yet to be returned), then no further books can be borrowed or reserved until all overdue books have been returned.
	4. A member can only reserve at most one book copy.
	5. A member cannot borrow another copy of the same book that has been previously borrowed.
	6. A member cannot reserve another copy of the same book previously borrowed.
	7. Any member can return his/her own borrowed book (even before it's due date).
	8. Members are only allowed to view their own borrowed/reserved books.
	9. Only members with full access to all operations (i.e Librarians a.k.a superusers or admins) are allowed to renew books and view all borrowed books.
