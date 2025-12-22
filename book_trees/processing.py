import ebooklib
import re
import spacy
from ebooklib import epub
from bs4 import BeautifulSoup
from django.db import transaction
from .models import EpubFile, Chapter, Character, Relationship

# load NLP
nlp = spacy.load("en_core_web_sm")

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
                chapter_number = int(match.group(1)) if match else None

                chapters.append({
                    'chapter_number': chapter_number,
                    'title': item.get_name(),
                    'content': text
                })

    return chapters

def process_epub_file(epub_id):

    epub = None
    try:
        epub = EpubFile.objects.get(id=epub_id)
        epub.status = 'pr'
        epub.save()

        file_path = epub.file.path

        chapters_data = extract_chapters_from_epub(file_path)

        for chapter_data in chapters_data:
            Chapter.objects.create(
                epub = epub,
                title=chapter_data['title'],
                content = chapter_data['content'],
                chapter_number = chapter_data['chapter_number']

            )

        epub.status = 'c'
        epub.processed = True
        epub.save()

        return True



    except Exception as e:
        if epub:
            epub.status = 'f'
            epub.error_message = str(e)
            epub.save()
        raise

def extract_characters_simple(epub_id):
    """
    Placeholder for character extraction.
    This will be implemented with spaCy/NLP later.
    """
    # TODO: Implement NER-based character extraction
    epub = EpubFile.objects.get(id=epub_id)
    chapters = epub.chapters.all()

    character_counts = {}
    first_appearance = {}


    for chapter in chapters:
        doc = nlp(chapter.content)

        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                name = ent.text.strip()

                #skip single letters, common false positive
                if len(name) <= 1:
                    continue

                character_counts[name] = character_counts.get(name, 0) + 1

                if name not in first_appearance:
                    first_appearance[name] = chapter.chapter_number

    # TODO: Create & save objects
    # for name, count in character_counts.items():
    #     Character.objects.update_or_create(
    #
    #     )

    print (character_counts)

    pass


def extract_relationships_simple(epub_id):
    """
    Placeholder for relationship extraction.
    This will be implemented with pattern matching or LLM later.
    """
    # TODO: Implement relationship extraction
    pass


