from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import EpubFile
from .forms import EpubUploadForm

def epub_list(request):
    """
    This view displays all uploaded EPUB files.

    1. Get all EpubFile objects from database
    2. Pass them to template
    3. Template displays in a nice way
    """

    # Query database for all EPUB files
    epubs = EpubFile.objects.all()

    # Render template with data
    # to template path
    # data being passed
    return render(request, 'book_trees/epub_list.html', {'epubs': epubs})

def upload_epub(request):
    """
    Handles upload form

    GET request: Show empty form
    POST request: Process uploaded form
    """

    if request.method == 'POST':
        form = EpubUploadForm(request.POST, request.FILES)

        if form.is_valid():
            epub = form.save()
            messages.success(request, 'EPUB Uploaded Successfully')

            # brings user back to the list page
            return redirect('epub_detail', pk=epub.pk)

        else:
            messages.error(request, 'Please correct the following errors:')

    elif request.method == 'GET':
        form = EpubUploadForm()

    return render(request, 'book_trees/upload.html', {'form' : form})


def epub_detail(request, pk):
    """
    Detailed view of single EPUB file

    pk: Primary Key of the EPUB file

    1. Get EPUB file with ID from database
    -> Doesn't exist: 404
    2. Pass to template
    """

    # tries to get object utilizing the pk value
    epub = get_object_or_404(EpubFile, pk=pk)

    return render(request, 'book_trees/epub_detail.html', {'epub' : epub})

def delete_epub(request, pk):
    """
    Delete a single EPUB file

    1. GET request: Confirm deletion
    2. POST request: Delete
    """

    epub = get_object_or_404(EpubFile, pk=pk)

    if request.method == 'POST':
        filename = epub.original_filename

        epub.file.delete()

        messages.success(request, f"Deleted: {filename}")

        return redirect('epub_list')

    return render(request, 'book_trees/confirm_delete.html', {'epub' : epub})

