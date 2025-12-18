from django import forms
from .models import EpubFile

class EpubUploadForm(forms.ModelForm):
    """
    Form is based on EpubFile model
    ModelForm auto creates input fields
    """

    class Meta:
        model = EpubFile            # model this form is for
        fields = ['file']           # field included in form

        widgets = {
            'file': forms.FileInput(attrs={
                'accept': '.epub',              # Shows only .epub files
                'class': 'form-control',        # Bootstrap CSS class
            })
        }

    def clean_file(self):
        """
        Validates upload file
        """

        file = self.cleaned_data.get('file')

        if file:
            #Check if file is .epub
            if not file.name.endswith('.epub'):
                raise forms.ValidationError('File must be .epub')

            if file.size > 50 * 1024 * 1024:
                raise forms.ValidationError('File must be less than 50MB')

        return file



    def save(self, commit=True):
        """
        Override save to set the original_filename automatically
        """

        # Create object (EpubFile) to be saved but don't actually save yet
        instance = super().save(commit=False)

        # copies down the current file name in to 'original_filename' before django renames it
        if instance.file:
            instance.original_filename = instance.file.name
        if commit:
            instance.save()
        return instance