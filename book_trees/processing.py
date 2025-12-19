import ebooklib
import re
from ebooklib import epub
from bs4 import BeautifulSoup
from django.db import transaction
from .models import EpubFile, Chapter, Character, Relationship


def extract_chapters_from_epub(epub_path):
    """Extract chapters and text from an EPUB file."""
    book = epub.read_epub(epub_path)
    chapters = []

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text = soup.get_text("\n", strip=True)

            if "chapter" in item.get_name().lower():
                match = re.search(r'chapter[_\s-]*(\d+)', item.get_name().lower())
                chapter_num = int(match.group(1)) if match else None

                chapters.append({
                    'number': chapter_num,
                    'title': item.get_name(),
                    'content': text[:250]
                })

    return chapters

def process_epub_file(epub_id):

    epub = None
    try:
        epub = EpubFile.objects.get(id=epub_id)
        epub.status = 'pr'
        epub.save()

        file_path = epub.file

        chapters_data = extract_chapters_from_epub(file_path)

        for chapter_data in chapters_data:
            print(f"{chapter_data}")

    except Exception as e:
        if epub:
            epub.status = 'f'
            epub.error_message = str(e)
            epub.save()
        raise




