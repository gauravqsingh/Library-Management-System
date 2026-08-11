import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Library_Management_System.settings')
django.setup()

from books.models import Book

# This instantly wipes out the broken image links across all books
Book.objects.all().update(image=None)

print("Successfully cleared all broken images so the blue gradient covers will show!")