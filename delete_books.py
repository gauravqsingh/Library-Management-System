import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Library_Management_System.settings')
django.setup()

from books.models import Book

# Target and delete only the automated books we just added
deleted_count, _ = Book.objects.filter(title__startswith="Mastering Code & Life").delete()

print(f"Successfully deleted {deleted_count} automated books!")