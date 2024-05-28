from django.shortcuts import render
from collect_files.tables import FileInSystemTable, SystemSampleTable
from django.views import generic

# Create your views here.
from .models import FileInSystem, SystemSample
from typing import Any
from django_tables2 import RequestConfig
from django.db.models import Q


class FilesView(generic.ListView):
    template_name = "collect_files/file_index.html"
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
                | Q(file_path__icontains=search_term)
                | Q(system_sample__sample_name__icontains=search_term)
            )

        files_table = FileInSystemTable(files_in_system)

        # Apply pagination
        page_number = kwargs.get("page", 1)
        files_table.paginate(per_page=25)
        # paginator = Paginator(files_table, 10)  # Show 10 rows per page
        RequestConfig(self.request, paginate={"per_page": 25}).configure(files_table)

        context["files_table"] = files_table
        context["search_term"] = search_term

        return context

    def get_queryset(self):
        return FileInSystem.objects.all()


class UploadIndexView(generic.TemplateView):
    template_name = "collect_files/upload.html"


class SamplesView(generic.TemplateView):
    template_name = "collect_files/sample_index.html"
    context_object_name = "sample_list"
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        samples_in_system = SystemSample.objects.all()

        # Get the search term from the request
        search_term = self.request.GET.get("search", "")

        # Filter the files based on the search term
        if search_term:
            samples_in_system = samples_in_system.filter(
                Q(sample_name__icontains=search_term)
                | Q(species__icontains=search_term)
                | Q(project__icontains=search_term)
                | Q(bioproject__icontains=search_term)
            )

        # sort by date earliest to latest
        samples_in_system = samples_in_system.order_by("-run_date")

        samples_table = SystemSampleTable(samples_in_system)

        # Apply pagination
        samples_table.paginate(per_page=25)
        # paginator = Paginator(files_table, 10)  # Show 10 rows per page
        RequestConfig(self.request, paginate={"per_page": 25}).configure(samples_table)

        context["samples_table"] = samples_table
        context["search_term"] = search_term

        return context

    def get_queryset(self):
        return SystemSample.objects.all()


import csv
from django.http import HttpResponse


def download_tsv(request):
    response = HttpResponse(content_type="text/tab-separated-values")
    response["Content-Disposition"] = 'attachment; filename="table.tsv"'

    writer = csv.writer(response, delimiter="\t")
    writer.writerow(
        [
            "Sample Name",
            "Species",
            "Department",
            "Project",
            "Bioproject",
            "Owner",
            "Run Date",
            "Files",
            "Fastq File Name",
        ]
    )  # Replace with your table headers

    for sample in SystemSample.objects.all():  # Replace with your queryset

        writer.writerow(
            [
                sample.sample_name,
                sample.species,
                sample.department,
                sample.project,
                sample.bioproject,
                sample.owner,
                sample.run_date_str,
                sample.nfiles,
                sample.fastq_file_name,
            ]
        )  # Replace with your table data

    return response
