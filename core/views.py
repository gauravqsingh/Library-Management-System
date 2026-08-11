from django.shortcuts import render
from books.models import Book
from books.constants import CATEGORY_CHOICES # Don't forget to import this!

def home_view(request, book_category=None):
    books = Book.objects.all()

    # This forces all categories from your constants file to show, and strips duplicates
    categories = list(dict.fromkeys([category[0].strip() for category in CATEGORY_CHOICES]))

    if book_category:
        books = books.filter(categories=book_category)

    return render(request, 'index.html', {
        'books': books,
        'categories': categories
    })