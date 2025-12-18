from django.db import models
from django.utils import timezone

# Create your models here.

class EpubFile(models.Model):
    file = models.FileField(upload_to='epubs/%Y/%m/%d')

    original_filename = models.CharField(max_length=255)

    uploaded_at = models.DateTimeField(default=timezone.now)
    processed = models.BooleanField(default=False)

    STATUS_CHOICES = [
        ('p', 'pending'),
        ('pr', 'processing'),
        ('c', 'completed'),
        ('f', 'failed'),
    ]
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='p')

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        return f"{self.original_filename} - {self.uploaded_at.strftime('%Y-%m-%d')}"