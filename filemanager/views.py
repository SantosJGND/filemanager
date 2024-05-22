from collect_files.models import (
    FileInSystem,
    UpdateSystemFiles,
    UpdateSystemSamples,
    SystemSample,
)

from typing import Any
from collect_files.tables import SystemSampleTable

from django.views import generic
from filemanager.settings import SOURCE_DATA_ROOT


class HomePageView(generic.TemplateView):
    template_name = "home.html"
    context_object_name = "file_list"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super(HomePageView, self).get_context_data(**kwargs)

        if UpdateSystemFiles.objects.all().exists():
            updates = UpdateSystemFiles.objects.all().order_by("-date").first()

            context["last_file_update"] = updates.date
        else:
            context["last_file_update"] = "Never"

        if UpdateSystemSamples.objects.all().exists():
            updates = UpdateSystemSamples.objects.all().order_by("-date").first()
            context["last_sample_update"] = updates.date
        else:
            context["last_sample_update"] = "Never"

        ####
        samples_in_system = SystemSample.objects.all().count()

        samples_without_files = SystemSample.objects.filter(
            fastq_file_name__in=["n.a.", "nan"]
        ).count()

        samples_with_files = SystemSample.objects.all().exclude(
            fastq_file_name__in=["n.a.", "nan"]
        )
        linked_samples = samples_with_files.exclude(system_sample_set=None).count()

        nsamples_missing_files = samples_with_files.filter(
            system_sample_set=None
        ).count()

        ####
        files_in_system = FileInSystem.objects.all().count()
        files_with_no_sample = FileInSystem.objects.filter(system_sample=None).count()
        files_with_sample = FileInSystem.objects.filter(
            system_sample__isnull=False
        ).count()

        context["files_in_system"] = files_in_system
        context["linked_samples"] = linked_samples
        context["samples_missing_files"] = nsamples_missing_files

        context["samples_without_files"] = samples_without_files
        context["linked_files"] = files_with_sample
        context["unlinked_files"] = files_with_no_sample
        context["scan_root"] = SOURCE_DATA_ROOT
        context["samples_in_system"] = samples_in_system

        return context
