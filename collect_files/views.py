from django.shortcuts import render
from collect_files.tables import FileInSystemTable
from django.views import generic

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from .models import FileInSystem
from typing import Any
from django_tables2 import RequestConfig
from django.core.paginator import Paginator
from django.db.models import Q


class FilesView(generic.ListView):
    template_name = "collect_files/index.html"
    context_object_name = "file_list"
    paginate_by = 10

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        files_in_system = FileInSystem.objects.all()

        # Get the search term from the request
        search_term = self.request.GET.get("search", "")

        # Filter the files based on the search term
        if search_term:
            files_in_system = files_in_system.filter(
                Q(file_name__icontains=search_term)
            )

        files_table = FileInSystemTable(files_in_system)

        # Apply pagination
        page_number = kwargs.get("page", 1)
        print(page_number)
        files_table.paginate(page=page_number, per_page=25)
        # paginator = Paginator(files_table, 10)  # Show 10 rows per page
        print(files_table)
        print("HOOO")

        # Pass the page object instead of the full table
        RequestConfig(self.request, paginate={"per_page": 25}).configure(files_table)

        context["files_table"] = files_table
        context["search_term"] = search_term

        return context

    def get_queryset(self):
        return FileInSystem.objects.all()


class UploadIndexView(generic.TemplateView):
    template_name = "collect_files/upload.html"
