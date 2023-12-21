from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Author, BookInstance, Genre, BookReview
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from catalog.forms import RenewBookForm, BookReviewForm, BookBorrowForm
from django.urls import reverse, reverse_lazy
import datetime
from django.contrib.auth.models import Group
from django.db.models import Count, Max
from django.core.exceptions import PermissionDenied
import random

# Create your views here.
@login_required
def index(request):
	"""View function for home page of site."""
	# Generate counts of some of the main objects
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()
	num_genres = Genre.objects.all().count()
	
	# Available books (status = 'a')
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()
	
	# The 'all()' is implied by default.
	num_authors = Author.objects.count()
	
	# Books that contain the word 'The' (case-insensitive)
	particular_books = Book.objects.filter(title__icontains='The').count()
	
	# number of visits made to this page
	num_visits = request.session.get('num_visits',0)
	request.session['num_visits'] = num_visits + 1
	
	context = {
		'num_books': num_books,
		'num_instances': num_instances,
		'num_instances_available': num_instances_available,
		'num_authors': num_authors,
		'num_genres': num_genres,
		'particular_books': particular_books,
		'num_visits': num_visits
	}
	
	# Render the HTML template index.html with the data in the context variable
	return render(request, 'index.html', context=context)

def sign_up(request):
	"""View function user registration."""
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			group = Group.objects.get(name="Library Members")
			user = form.save()
			user.groups.add(group)
			messages.success(request,f'Hi {username}, your new account has been created. You can now log in with your credentials.')
			return redirect('login')
	else:
		form = UserCreationForm()
		
	context = {'form':form}
	
	return render(request,'registration/sign_up.html',context)


class BookListView(LoginRequiredMixin,ListView):
	"""View function to retrieve list of all books."""
	model = Book
	template_name = 'book_list.html'
	paginate_by = 9
	
	def get_queryset(self):
		return Book.objects.all().order_by('title')

	def get_context_data(self,**kwargs):
		data = BookInstance.objects.filter(status='o').values('book').annotate(book_count=Count('id')).order_by('book_count').last()
		book = Book.objects.get(pk=data['book'])
		latest_book = Book.objects.all().order_by('date').last()
		recently_borrowed = BookInstance.objects.filter(borrower=self.request.user,status='o').order_by('updated').last()
		all_books = Book.objects.all()
		count_books = Book.objects.all().count()
		recommended_book = all_books[random.randint(0,count_books - 1)]
		context = super().get_context_data(**kwargs)
		context['favorite'] = book
		context['latest_book'] = latest_book
		context['recently_borrowed'] = recently_borrowed
		context['recommended_book'] = recommended_book
		return context

@login_required
def book_detail(request,pk):
	"""View function to retrieve specific details of each book."""
	book = Book.objects.get(id=pk)
	if request.method == 'POST':
		form = BookReviewForm(request.POST)
		if form.is_valid():
			review = form.cleaned_data['review']
			user = request.user
			BookReview.objects.create(review=review,book=book,user=user)
			form = BookReviewForm()
			context = {'book':book,'form':form}
	else:
		form = BookReviewForm()
		context = {'book':book,'form':form}
		
	return render(request,'book_detail.html',context=context)


class AuthorListView(LoginRequiredMixin,ListView):
	model = Author
	template_name = 'author_list.html'
	paginate_by = 9

class AuthorDetailView(LoginRequiredMixin,DetailView):
	model = Author
	template_name = 'author_detail.html'

def review_delete(request,pk):
	"""View function to delete reviews of each book."""
	review = get_object_or_404(BookReview, id=pk)
	if request.method == 'POST':
		if review.user == request.user:
			review.delete()
			return redirect(reverse('book-detail',args=[str(review.book.id)]))
		else:
			raise PermissionDenied
	else:
		context = {'post':review}
		
	return render(request, 'review_delete.html',context=context)

@login_required
def book_return(request,id):
	"""View function to return copies of books."""
	book = Book.objects.get(pk=id)
	books_borrowed = BookInstance.objects.filter(book=book,borrower=request.user,status='o').first()
	books_reserved = BookInstance.objects.filter(book=book,borrower=request.user,status='r').first()
	book_instance = books_borrowed or books_reserved
	if request.method == 'POST':
		if request.user == book_instance.borrower:
			book_instance.borrower = None
			book_instance.status = 'a'
			book_instance.due_back = None
			book_instance.save()
			messages.success(request,f'{book} has been returned successfully')
			return redirect('my-borrowed')
		else:
			raise PermissionDenied
	else:
		context = {'book_instance':book_instance}
		return render(request,'confirm_return.html',context)

class GenreListView(LoginRequiredMixin, ListView):
	"""View function to retrieve list of genres."""
	model = Genre
	template_name = 'genre_list.html'
	paginate_by = 10

class GenreDetailView(LoginRequiredMixin, DetailView):
	model = Genre
	template_name = 'genre_detail.html'

class CopyListView(LoginRequiredMixin, ListView):
	"""View function to retrieve book instance copies."""
	model = BookInstance
	template_name = 'copy_list.html'
	paginate_by = 10

class LoanedBooksByUserListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
	"""Generic class-based view listing books on loan to current user."""
	model = BookInstance
	template_name = 'bookinstance_list_borrowed_user.html'
	permission_required = 'catalog.can_mark_returned' # field attributes used by class-based views to check for permissions
	
	def get_queryset(self):
		return (
			BookInstance.objects.filter(borrower=self.request.user)
			.filter(status__exact='o')
			.order_by('due_back')
		)
	
	def get_context_data(self,**kwargs):
		data = BookInstance.objects.filter(borrower=self.request.user,status='r')
		context = super().get_context_data(**kwargs)
		context['reserved_books'] = data
		return context

class LoanedBooksByAllUsersListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
	"""Generic class-based view listing all books on loan."""
	model = BookInstance
	template_name = 'librarians_all_books.html'
	permission_required = 'catalog.can_mark_returned'
	paginate_by = 10
	
	def get_queryset(self):
		if self.request.user.is_superuser:
			return BookInstance.objects.filter(status='o').order_by('book__title')
		else:
			raise PermissionDenied

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
	"""View function for renewing a specific BookInstance by librarian."""
	book_instance = get_object_or_404(BookInstance, pk=pk)
	
	# If this is a POST request then process the Form data
	if request.method == 'POST':
		
		# Create a form instance and populate it with data from the request (binding):
		form = RenewBookForm(request.POST)
		
		# Check if the form is valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required (here we just write it to the model due_back field)
			book_instance.due_back = form.cleaned_data['renewal_date']
			book_instance.save()
			
			# redirect to a new URL:
			return redirect('all-borrowed')
		
		# If this is a GET (or any other method) create the default form.
	else:
		proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
		form = RenewBookForm()

	context = {
		'form': form,
		'book_instance': book_instance,
	}
	
	if request.user.is_superuser:
		return render(request, 'book_renew_librarian.html', context)
	else:
		raise PermissionDenied

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def book_borrow(request,pk):
	"""View function to borrow or reserve specific copies of each book."""
	book = get_object_or_404(Book,pk=pk)
	message = None
	collection = None
	if request.method == 'POST':
		count = 0
		for books in BookInstance.objects.filter(status__exact='o'):
			if books.borrower == request.user:
				count += 1
		if count == 3:
			message = "You have already reached your borrowing limit - **3 books**"
			warning = "borrowed limit"
		else:
			collection = []
			for books in BookInstance.objects.filter(status__exact='o'):
				if books.borrower == request.user and books.is_overdue:
					collection.append(books)
			if collection:
				message = "You are yet to return the following books:"
				warning = "books due"
			else:
				post = request.POST.copy()
				post['book'] = book.title
				request.POST = post
				form = BookBorrowForm(request.POST)
				if form.is_valid():
					action = form.cleaned_data['action']
					bookinstance = BookInstance.objects.filter(book__title=book.title).filter(status__exact='a').first()
					if bookinstance:
						if action == 'borrow':
							reserved_book = BookInstance.objects.filter(book=book,borrower=request.user,status='r').first()
							if reserved_book and reserved_book.book.title == bookinstance.book.title:
								reserved_book.due_back = form.cleaned_data['return_date']
								reserved_book.borrower = request.user
								reserved_book.status = 'o'
								reserved_book.save()
							else:
								loaned_book = BookInstance.objects.filter(book=book,borrower=request.user,status='o').first()
								if loaned_book:
									message = "You have already loaned a copy of this book."
									warning = "loaned before"
									context = {'message':message,'warning':warning}
									return render(request, 'borrow_unallowed.html', context)
								else:
									bookinstance.due_back = form.cleaned_data['return_date']
									bookinstance.borrower = request.user
									bookinstance.status = 'o'
									bookinstance.save()
						elif action == 'reserve':
							reserved_books = 0
							for reserved in BookInstance.objects.filter(borrower=request.user,status='r'):
								reserved_books += 1
							if reserved_books:
								message = "Limit reached - You cannot reserve more than one book."
								warning = "reservation limit"
								context = {'message':message,'warning':warning}
								return render(request, 'borrow_unallowed.html', context)
							else:
								loaned_book = BookInstance.objects.filter(book=book,borrower=request.user,status='o').first()
								if loaned_book:
									message = "You already have a copy of this book."
									warning = "loaned before"
									context = {'message':message,'warning':warning}
									return render(request, 'borrow_unallowed.html', context)
								else:
									bookinstance.due_back = form.cleaned_data['return_date']
									bookinstance.borrower = request.user
									bookinstance.status = 'r'
									bookinstance.save()
						if action == 'borrow':
							if reserved_book and reserved_book.book.title == bookinstance.book.title:
								messages.success(request,f'You have successfully borrowed your reserved copy of "{reserved_book.book.title}"')
								return redirect(reverse('book-borrow',args=[str(book.id)]))
							else:
								messages.success(request,f'You have successfully borrowed a copy of "{bookinstance.book.title}"')
								return redirect(reverse('book-borrow',args=[str(book.id)]))
						else:
							messages.success(request,f'You have successfully reserved a copy of "{bookinstance.book.title}"')
							return redirect(reverse('book-borrow',args=[str(book.id)]))
					else:
						messages.error(request,'There are no available copies of this book')
						return redirect(reverse('book-borrow',args=[str(book.id)]))

	else:
		form = BookBorrowForm(initial={'book':book.title})
		

	if collection:
		context = {'message':message,'warning':warning,'collection':collection}
		return render(request, 'borrow_unallowed.html', context)
	elif message:
		context = {'message':message,'warning':warning}
		return render(request, 'borrow_unallowed.html', context)
	
	context={'form':form}
	
	return render(request, 'book_borrow_form.html', context=context)
