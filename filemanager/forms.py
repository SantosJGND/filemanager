from django import forms
from collect_files.models import UpdateSystemFiles

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UpdateSystemFiles
        fields = ['file', 'contact']