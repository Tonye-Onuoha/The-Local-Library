import datetime

from django.test import SimpleTestCase
from django.utils import timezone

from catalog.forms import RenewBookForm,BookReviewForm,BookBorrowForm

class RenewBookFormTest(SimpleTestCase):
    def test_renew_form_date_field_label(self):
        form = RenewBookForm()
        self.assertTrue(form.fields['renewal_date'].label is None or form.fields['renewal_date'].label == 'renewal date')
        # Django returns None if a label value isn't explicitly set (it eventually creates a label for you using the field name)

    def test_renew_form_date_field_help_text(self):
        form = RenewBookForm()
        self.assertEqual(form.fields['renewal_date'].help_text, 'Enter a date between now and 4 weeks (default 3).')

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        date = timezone.localtime() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())
		
class BookReviewFormTest(SimpleTestCase):
	def test_review_label(self):
		form = BookReviewForm()
		label = form.fields['review'].label
		self.assertTrue(label == "")
		
	def test_review_help_text(self):
		form = BookReviewForm()
		help_text = form.fields['review'].help_text
		self.assertEqual(help_text,'Please kindly leave a review about this book.')
		
	def test_review_max_length(self):
		form = BookReviewForm()
		max_length = form.fields['review'].max_length
		self.assertEqual(max_length,150)
		
class BookBorrowFormTest(SimpleTestCase):
	def test_book_label(self):
		form = BookBorrowForm()
		label = form.fields['book'].label
		self.assertTrue(label is None or label == 'book')
		
	def test_book_help_text(self):
		form = BookBorrowForm()
		help_text = form.fields['book'].help_text
		self.assertEqual(help_text,'Enter a book')
		
	def test_action_label(self):
		form = BookBorrowForm()
		label = form.fields['action'].label
		self.assertEqual(label,'What do you want to do ?')
		
	def test_return_date_label(self):
		form = BookBorrowForm()
		label = form.fields['return_date'].label
		self.assertTrue(label is None or label == 'return date')
		
	def test_return_date_help_text(self):
		form = BookBorrowForm()
		help_text = form.fields['return_date'].help_text
		self.assertEqual(help_text,'Enter the date to be returned/unreserved')
		
	def test_action_borrow_field(self):
		date = datetime.date.today()
		form = BookBorrowForm(data={'book':'The Client','return_date':date,'action':'borrow'})
		self.assertTrue(form['book'].value() == 'The Client')
		self.assertEqual(form['action'].value(),'borrow')
		
	def test_action_reserve_field(self):
		date = datetime.date.today()
		form = BookBorrowForm(data={'book':'The Client','return_date':date,'action':'reserve'})
		self.assertEqual(form['book'].value(),'The Client')
		self.assertEqual(form['action'].value(),'reserve')
		
	def test_return_date_in_the_past(self):
		date = datetime.date.today() - datetime.timedelta(days=7)
		form = BookBorrowForm({'book':'The Client','return_date':date,'action':'borrow'})
		self.assertEqual(form.data['action'],'borrow')
		self.assertFalse(form.is_valid())
		
	def test_return_date_too_far_in_the_future(self):
		date = datetime.date.today() - datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
		form = BookBorrowForm({'book':'The Client','return_date':date,'action':'borrow'})
		self.assertEqual(form.data['action'],'borrow')
		self.assertFalse(form.is_valid())
		
	# form fields can be accessed by either form['field'].value() or form.data['field]

