from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from .models import FileInSystem

class FilesTable(generic.ListView):
    template_name = 'collect_files/index.html'
    context_object_name = 'file_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return FileInSystem.objects.order_by('-file_date')[:5]

    