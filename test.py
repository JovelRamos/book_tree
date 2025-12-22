import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_tree.settings')
django.setup()

from book_trees.processing import extract_characters_simple

extract_characters_simple(1)  # Use your epub ID