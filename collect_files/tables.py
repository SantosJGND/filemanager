from collect_files.models import FileInSystem, SystemSample
from django.shortcuts import render
from django.views import generic
import django_tables2 as tables


class FileInSystemTable(tables.Table):
    model = FileInSystem
    size = tables.Column(empty_values=(), verbose_name="Size")
    system_sample = tables.Column(empty_values=(), verbose_name="Sample")

    class Meta:
        model = FileInSystem
        template_name = "django_tables2/bootstrap.html"
        fields = ("file_name", "system_sample", "file_path")
        attrs = {
            "class": "files-table table-striped table-bordered table-hover",
            "th": {"class": "files-table-header"},
            "td": {"class": "files-table-data"},
        }

    def render_size(self, value, record: FileInSystem) -> str:
        return f"{record.file_size} bytes"

    def render_system_sample(self, value, record: FileInSystem) -> str:
        sample = record.system_sample
        if sample:
            return sample.sample_name
        return "No sample"


from django.db.models import Count, F


class SystemSampleTable(tables.Table):
    model = SystemSample

    files = tables.Column(empty_values=(), verbose_name="Files")

    class Meta:
        model = SystemSample
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "sample_name",
            "species",
            "project",
            "bioproject",
            "owner",
            "files",
            "run_date",
            "fastq_file_name",
        )
        attrs = {
            "class": "files-table table-striped table-bordered table-hover",
            "th": {"class": "files-table-header"},
            "td": {"class": "files-table-data"},
            "nav": {"class": "pagination"},
        }

    def render_files(self, value, record: SystemSample) -> str:
        nfiles = FileInSystem.objects.filter(system_sample=record).count()

        return f"{nfiles} files"

    def order_files(self, queryset, is_descending):
        queryset = queryset.annotate(nfiles=Count("files")).order_by(
            F("nfiles").desc(nulls_last=True)
        )
        return (queryset, True)
