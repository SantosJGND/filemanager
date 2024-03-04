from collect_files.models import FileInSystem, SystemSample
from django.shortcuts import render
from django.views import generic
import django_tables2 as tables


class FileInSystemTable(tables.Table):
    model = FileInSystem
    size = tables.Column(empty_values=(), verbose_name="Size")

    class Meta:
        model = FileInSystem
        template_name = "django_tables2/bootstrap.html"
        fields = ("file_name", "file_path")
        attrs = {
            "class": "files-table table-striped table-bordered table-hover",
            "th": {"class": "files-table-header"},
            "td": {"class": "files-table-data"},
        }

    def render_size(self, value, record: FileInSystem) -> str:
        return f"{record.file_size} bytes"


class SystemSampleTable(tables.Table):
    model = SystemSample

    class Meta:
        model = SystemSample
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "sample_name",
            "species",
            "project",
            "bioproject",
            "owner",
            "run_date",
        )
        attrs = {
            "class": "files-table table-striped table-bordered table-hover",
            "th": {"class": "files-table-header"},
            "td": {"class": "files-table-data"},
        }
