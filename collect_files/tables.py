from collect_files.models import FileInSystem
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
