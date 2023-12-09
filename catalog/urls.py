from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.sign_up, name='sign-up'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.book_detail, name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('librarian-books,', views.LoanedBooksByAllUsersListView.as_view(), name='all-borrowed'),
    path('book-borrow/<int:pk>/', views.book_borrow, name='book-borrow'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
	path('return-book/<int:id>/',views.book_return,name='book-return'),
    path('review/<int:pk>', views.review_delete, name='review-delete'),
    path('genres/', views.GenreListView.as_view(), name='genres'),
    path('genres/<int:pk>/', views.GenreDetailView.as_view(), name='genre-detail'),
    path('copies/', views.CopyListView.as_view(), name='copies'),
]
