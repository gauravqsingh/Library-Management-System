import os
import django
import random
import requests
from django.core.files.base import ContentFile

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Library_Management_System.settings')
django.setup()

from books.models import Book

categories_list = ['Fiction', 'Mystery', 'History', 'Non-Fiction', 'Cookbook', 'Romance']

print("Generating 300 books with unique covers... Please wait a moment.")

for i in range(1, 301):
    title = f"Mastering Code & Life - Vol. {i}"
    price = round(random.uniform(12.99, 49.99), 2)
    category = random.choice(categories_list)
    description = f"This is an automated library inventory description for volume number {i}. Packed with amazing insights and stories."

    # Create the book instance
    book = Book(
        title=title,
        price=price,
        categories=category,
        description=description
    )

    # Fetch a unique cover image using an image seed (ensures every book gets a unique photo)
    image_url = f"https://picsum.photos/seed/library_book_{i}/300/400"

    try:
        response = requests.get(image_url, timeout=5)
        if response.status_code == 200:
            # Save the downloaded image file into Django's ImageField
            book.image.save(f"cover_{i}.jpg", ContentFile(response.content), save=False)
    except Exception as e:
        print(f"Skipped image for book {i} due to network timeout.")

    book.save()

    if i % 50 == 0:
        print(f"Processed {i} books...")

print("Successfully generated and added 300 books with unique individual covers!")