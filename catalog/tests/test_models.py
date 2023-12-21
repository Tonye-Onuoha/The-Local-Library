from django.test import TestCase
from catalog.models import Author,Genre,Book,BookInstance,BookReview
from django.contrib.auth.models import User
import datetime

# Create your tests here.
class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        author = Author.objects.all().first()
        field_name = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_name,'last name')

    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_name = author._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_name,'date of birth')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'Died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEqual(max_length,100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(str(author), expected_object_name)

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1/')
		
class GenreModelTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		Genre.objects.create(name='Horror')
		
	def test_name_label(self):
		genre = Genre.objects.get(id=1)
		label = genre._meta.get_field('name').verbose_name
		self.assertEqual(label,'name')
		
	def test_name_help_text(self):
		genre = Genre.objects.get(id=1)
		help_text = genre._meta.get_field('name').help_text
		self.assertEqual(help_text,'Enter a book genre (e.g. Science Fiction)')
		
	def test_name_max_length(self):
		genre = Genre.objects.get(id=1)
		max_length = genre._meta.get_field('name').max_length
		self.assertEqual(max_length,200)
		
	def test_genre_name(self):
		genre = Genre.objects.get(id=1)
		expected_name = f'{genre.name}'
		self.assertEqual(expected_name,'Horror')

	def test_string_representation(self):
		genre = Genre.objects.get(id=1)
		self.assertEqual(str(genre),'Horror')
		
		
class BookModelTest(TestCase):
	def setUp(self):
		# Create an author
		test_author = Author.objects.create(first_name='John', last_name='Grisham')
		# Create some genres
		Genre.objects.create(name='Fiction')
		Genre.objects.create(name='Legal Thriller')
		# Create a book
		book = Book.objects.create(title='The Client',author=test_author,summary='The Client is a legal thriller written by American author John Grisham, set mostly in Memphis, Tennessee, and New Orleans, Louisiana. It is Grisham\'s fourth novel',isbn='0099537087')
		
		# Create genre as a post-step
		book_genres = Genre.objects.all()
		book.genre.set(book_genres) # Direct assignment of many-to-many types not allowed.
		book.save()
		
	def test_title_label(self):
		book = Book.objects.get(id=1)
		label = book._meta.get_field('title').verbose_name
		self.assertEqual(label,'title')
		
	def test_title_max_length(self):
		book = Book.objects.get(id=1)
		max_length = book._meta.get_field('title').max_length
		self.assertEqual(max_length,200)
			
	def test_book_title(self):
		book = Book.objects.get(id=1)
		expected_title = f'{book.title}'
		self.assertEqual(expected_title,'The Client')
			
	def test_author_label(self):
		book = Book.objects.get(id=1)
		label = book._meta.get_field('author').verbose_name
		self.assertEqual(label,'author')
			
	def test_book_author(self):
		book = Book.objects.get(id=1)
		expected_author = 'Grisham, John'
		self.assertEqual(expected_author,str(book.author))
			
	def test_summary_label(self):
		book = Book.objects.get(id=1)
		label = book._meta.get_field('summary').verbose_name
		self.assertEqual(label,'summary')
			
	def test_summary_max_length(self):
		book = Book.objects.get(id=1)
		max_length = book._meta.get_field('summary').max_length
		self.assertEqual(max_length,1000)
			
	def test_summary_help_text(self):
		book = Book.objects.get(id=1)
		help_text = book._meta.get_field('summary').help_text
		self.assertEqual(help_text,'Enter a brief description of the book')
			
	def test_isbn_label(self):
		book = Book.objects.get(id=1)
		label = book._meta.get_field('isbn').verbose_name
		self.assertEqual(label,'ISBN')
			
	def test_isbn_max_length(self):
		book = Book.objects.get(id=1)
		max_length = book._meta.get_field('isbn').max_length
		self.assertEqual(max_length,13)
			
	def test_isbn_help_text(self):
		book = Book.objects.get(id=1)
		help_text = book._meta.get_field('isbn').help_text
		self.assertEqual(help_text,'13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
			
	def test_string_representation(self):
		book = Book.objects.get(id=1)
		self.assertEqual(str(book),'The Client')
			
	def test_get_absolute_url(self):
		book = Book.objects.get(id=1)
		self.assertEqual(book.get_absolute_url(),'/catalog/book/1/')
		
		
		
class BookInstanceModelTest(TestCase):
	def setUp(self):
		# Create an author
		test_author = Author.objects.create(first_name='John', last_name='Grisham')
		# Create some genres
		Genre.objects.create(name='Fiction')
		Genre.objects.create(name='Legal Thriller')
		# Create a book
		test_book = Book.objects.create(title='The Client',author=test_author,summary='The Client is a legal thriller written by American author John Grisham, set mostly in Memphis, Tennessee, and New Orleans, Louisiana. It is Grisham\'s fourth novel',isbn='0099537087')
		
		# Create genre as a post-step
		book_genres = Genre.objects.all()
		test_book.genre.set(book_genres) # Direct assignment of many-to-many types not allowed.
		test_book.save()
		
		# Create a user/borrower
		test_user = User.objects.create_user(username='john',password='zGXn9dk143')
		
		# Create a book instance
		return_date = datetime.date.today() + datetime.timedelta(days=3)
		BookInstance.objects.create(book=test_book,imprint='The Client by John Grisham',due_back=return_date,borrower=test_user)
		
	def test_id_label(self):
		book_instance = BookInstance.objects.all().last()
		label = book_instance._meta.get_field('id').verbose_name
		self.assertEqual(label,'id')
			
	def test_id_help_text(self):
		book_instance = BookInstance.objects.all().last()
		help_text = book_instance._meta.get_field('id').help_text
		self.assertEqual(help_text,'Unique ID for this particular book across whole library')
			
	def test_book_instance_book(self):
		book_instance = BookInstance.objects.all().last()
		expected_title = 'The Client'
		# assert book title
		self.assertEqual(expected_title,f'{book_instance.book.title}')
		# assert book author
		expected_author = 'John Grisham'
		self.assertEqual(expected_author,f'{book_instance.book.author.first_name} {book_instance.book.author.last_name}')
			
	def test_imprint_label(self):
		book_instance = BookInstance.objects.all().last()
		label = book_instance._meta.get_field('imprint').verbose_name
		self.assertEqual(label,'imprint')
			
	def test_imprint_max_length(self):
		book_instance = BookInstance.objects.all().last()
		max_length = book_instance._meta.get_field('imprint').max_length
		self.assertEqual(max_length,200)
		
	def test_book_instance_borrower(self):
		book_instance = BookInstance.objects.all().last()
		expected_borrower = 'john'
		self.assertEqual(expected_borrower,str(book_instance.borrower))
		
	def test_book_instance_status(self):
		book_instance = BookInstance.objects.all().last()
		expected_status = 'm' # This is the default
		self.assertEqual(expected_status,f'{book_instance.status}')
		
	def test_book_instance_is_overdue(self):
		book_instance = BookInstance.objects.all().last()
		self.assertFalse(book_instance.is_overdue)
		
		
class BookReviewModelTest(TestCase):
	def setUp(self):
		# Create an author
		test_author = Author.objects.create(first_name='John', last_name='Grisham')
		# Create some genres
		Genre.objects.create(name='Fiction')
		Genre.objects.create(name='Legal Thriller')
		# Create a book
		test_book = Book.objects.create(title='The Client',author=test_author,summary='The Client is a legal thriller written by American author John Grisham, set mostly in Memphis, Tennessee, and New Orleans, Louisiana. It is Grisham\'s fourth novel',isbn='0099537087')
		
		# Create genre as a post-step
		book_genres = Genre.objects.all()
		test_book.genre.set(book_genres) # Direct assignment of many-to-many types not allowed.
		test_book.save()
		
		# Create a user
		test_user = User.objects.create_user(username='john',password='zGXn9dk143')
		
		# Create a review
		BookReview.objects.create(review='This book is an absolute masterpiece',book=test_book,user=test_user)
		
	def test_review_label(self):
		review_instance = BookReview.objects.get(id=1)
		label = review_instance._meta.get_field('review').verbose_name
		self.assertEqual(label,'review')
		
	def test_review_max_length(self):
		review_instance = BookReview.objects.get(id=1)
		max_length = review_instance._meta.get_field('review').max_length
		self.assertEqual(max_length,150)
		
	def test_review_help_text(self):
		review_instance = BookReview.objects.get(id=1)
		help_text = review_instance._meta.get_field('review').help_text
		self.assertEqual(help_text,'Please kindly leave a review')
		
	def test_book_review(self):
		review_instance = BookReview.objects.get(id=1)
		expected_review = 'This book is an absolute masterpiece'
		self.assertEqual(expected_review,f'{review_instance.review}')
		
	def test_review_book(self):
		review_instance = BookReview.objects.get(id=1)
		expected_book = 'The Client'
		expected_author = 'John Grisham'
		self.assertEqual(expected_book,f'{review_instance.book.title}')
		self.assertEqual(expected_author,f'{review_instance.book.author.first_name} {review_instance.book.author.last_name}')
		
	def test_review_user(self):
		review_instance = BookReview.objects.get(id=1)
		expected_user = 'john'
		self.assertEqual(expected_user,str(review_instance.user))
		
		
		
			
		
		
		
		
		
			
		
		
		
		

		
