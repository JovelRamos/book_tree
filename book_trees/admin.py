from django.contrib import admin
from .models import EpubFile

# Register your models here.

@admin.register(EpubFile)
class EpubFileAdmin(admin.ModelAdmin):
    list_display = ['original_filename', 'status', 'uploaded_at', 'processed']
    list_filter =  ['status', 'processed', 'uploaded_at']
    search_fields = ['original_filename']
    readonly_fields = ['uploaded_at']
