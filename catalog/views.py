from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Author, BookInstance, Genre
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from catalog.forms import RenewBookForm
from django.urls import reverse, reverse_lazy
import datetime

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
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            form.save()
            messages.success(request,f'Hi {username}, your new account has been created. You can now log in with your credentials.')
            return redirect('login')
    else:
        form = UserCreationForm()

    context = {'form':form}

    return render(request,'registration/sign_up.html',context)



class BookListView(LoginRequiredMixin,ListView):
    model = Book
    template_name = 'book_list.html'

    def get_queryset(self):
        return Book.objects.all().order_by('title')


class BookDetailView(LoginRequiredMixin,DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'


class AuthorListView(LoginRequiredMixin,ListView):
    model = Author
    template_name = 'author_list.html'
    paginate_by = 10


class AuthorDetailView(LoginRequiredMixin,DetailView):
    model = Author
    template_name = 'author_detail.html'


class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}
    template_name = 'author_form.html'

class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)
    template_name = 'author_form.html'

class AuthorDelete(DeleteView):
    model = Author
    template_name = 'author_confirm_delete.html'
    success_url = reverse_lazy('authors')


class LoanedBooksByUserListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned' # field attributes used by class-based views to check for permissions

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )

class LoanedBooksByLibrariansListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = BookInstance
    template_name = 'librarians.html'
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status='o').order_by('book__title')


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
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'book_renew_librarian.html', context)
