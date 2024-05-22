from collect_files.models import (
    FileInSystem,
    UpdateSystemFiles,
    UpdateSystemSamples,
    SystemSample,
)

from typing import Any

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

        files_in_system = FileInSystem.objects.all().count()
        samples_in_system = SystemSample.objects.all().count()

        files_with_no_sample = FileInSystem.objects.filter(system_sample=None).count()
        files_with_sample = FileInSystem.objects.filter(
            system_sample__isnull=False
        ).count()

        context["files_in_system"] = files_in_system
        context["linked_files"] = files_with_sample
        context["unlinked_files"] = files_with_no_sample
        context["scan_root"] = SOURCE_DATA_ROOT
        context["samples_in_system"] = samples_in_system

        return context
