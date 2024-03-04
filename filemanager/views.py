from collect_files.models import FileInSystem, UpdateSystemFiles
from collect_files.tables import FileInSystemTable
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from typing import Any
import os

from django.views import generic
from django.core.paginator import Paginator


class HomePageView(generic.TemplateView):
    template_name = "home.html"
    context_object_name = "file_list"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super(HomePageView, self).get_context_data(**kwargs)

        if UpdateSystemFiles.objects.all().exists():
            updates = UpdateSystemFiles.objects.all().order_by("-date").first()
            print(updates.date)
            context["last_update"] = updates.date
        else:
            context["last_update"] = "Never"

        files_in_system = FileInSystem.objects.all().count()

        context["files_in_system"] = files_in_system

        return context
