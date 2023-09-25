from django.contrib import admin
from .models import Book, BookInstance, Author, Genre, BookReview

# Register your models here.
#admin.site.register(Book)
#admin.site.register(BookInstance)
#admin.site.register(Author)
#admin.site.register(Genre)

# create an inline class
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

# create an inline class
class BookInline(admin.TabularInline):
    model = Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre') # Defines the fields that are shown in the list-view of the admin
    # fieldsets attribute is used to divide the model detail view into sections
    fieldsets = (
            (
            None,{'fields':('title', 'author', 'cover')})
            ,
            (
            'Details',{'fields':('genre','summary')})
        )
    inlines = [BooksInstanceInline] # inlines are used to make associated models appear on the same detail view


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'imprint', 'due_back', 'status', 'borrower')
    list_filter = ('status',) # Gives us the ability to filter by status


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    # Defines the order of the fields and how they are laid out (tuple:horizontal,no tuple:vertical) in the detail view
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('review', 'book', 'date', 'user')
    list_filter = ('book',)



admin.site.register(Book,BookAdmin)
admin.site.register(BookInstance,BookInstanceAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(Genre)
