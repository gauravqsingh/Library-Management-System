import os
import json
import random
import time
import urllib.request
from urllib.error import HTTPError

# 1. Initialize the Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Library_Management_System.settings')
import django
django.setup()

# 2. Import Django tools and your models
from django.core.files.base import ContentFile
from books.models import Book
from books.constants import CATEGORY_CHOICES

def seed_database(target_total=1000):
    categories = [choice[0] for choice in CATEGORY_CHOICES]
    books_per_cat = (target_total // len(categories)) + 1
    books_added = 0

    print(f"🚀 Bypassing Google... Switching to Open Library API.")
    print(f"Targeting {target_total} books. This will take a few minutes.\n")

    for category in categories:
        print(f"--- Fetching category: {category} ---")

        # Open Library pagination uses an 'offset'
        for offset in range(0, books_per_cat, 40):
            # Clean category name for the URL (e.g., "Non-Fiction" -> "non_fiction")
            clean_cat = category.lower().replace(" ", "_").replace("-", "_")
            url = f"https://openlibrary.org/subjects/{clean_cat}.json?limit=40&offset={offset}"

            time.sleep(1) # Be polite to the Open Library servers

            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'LibraryPortalBot/1.0'})
                with urllib.request.urlopen(req) as response:
                    data = json.loads(response.read().decode())

                    works = data.get('works', [])
                    if not works:
                        break # No more books in this category

                    for work in works:
                        if books_added >= target_total:
                            print("\n✅ Successfully seeded 1,000 books into the database!")
                            return

                        title = work.get('title', 'Unknown Title')

                        # Skip if this book is already in your database
                        if Book.objects.filter(title=title[:100]).exists():
                            continue

                        # Extract authors to make a description (since OpenLibrary subject API omits descriptions)
                        authors = [a.get('name') for a in work.get('authors', [])]
                        author_str = ", ".join(authors) if authors else "Unknown Author"
                        description = f"A fascinating {category} book by {author_str}. (Data provided by Open Library)."

                        # Generate a random price between $9.99 and $49.99
                        price = round(random.uniform(9.99, 49.99), 2)

                        book = Book(
                            categories=category,
                            title=title[:100],
                            description=description,
                            price=price
                        )

                        # 3. Handle Cover Image Downloading
                        cover_id = work.get('cover_id')
                        if cover_id:
                            image_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
                            try:
                                img_req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
                                with urllib.request.urlopen(img_req) as img_response:
                                    safe_title = "".join([c for c in title[:20] if c.isalpha() or c.isdigit()]).rstrip()
                                    img_filename = f"{safe_title}_{random.randint(100,999)}.jpg"
                                    book.image.save(img_filename, ContentFile(img_response.read()), save=False)
                            except Exception:
                                pass # Skip image if it fails to download

                        # 4. Save to Database
                        book.save()
                        books_added += 1
                        print(f"[{books_added}/{target_total}] Added: {book.title}")

            except HTTPError as e:
                print(f"⚠️ Error on category '{category}': {e}")
                break
            except Exception as e:
                print(f"⚠️ Unexpected error fetching {category}: {e}")

if __name__ == '__main__':
    seed_database(1000)