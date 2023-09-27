import datetime
import os
from pathlib import Path

from collect_files.models import FileInSystem
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from filemanager.settings import SOURCE_DATA_ROOT


def match_file_pattern(file_name):
    if ".fastq" in file_name:
        return True

    return False


def check_if_symbolic_link(file_path):
    return os.path.islink(file_path)


def get_file_info(file_path):
    if check_if_symbolic_link(file_path):
        file_path = os.readlink(file_path)

    if os.path.exists(file_path) is False:
        file_size = 0
        file_deleted = True
        file_date = timezone.now()
    else:
        file_size = os.path.getsize(file_path)
        file_deleted = False
        file_date = timezone.make_aware(
            datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
        )

    file_path = Path(file_path)
    file_name = file_path.name

    file_type = file_path.suffix

    file_hash = "not implemented yet"

    return file_name, file_size, file_type, file_date, file_hash, file_deleted


def update_file_info(file_path):
    file_name, file_size, file_type, file_date, file_hash, file_deleted = get_file_info(
        file_path
    )
    try:
        file_in_system = FileInSystem.objects.get(file_path=file_path)

    except FileInSystem.DoesNotExist:
        file_in_system = FileInSystem()
        file_in_system.file_path = file_path
        file_in_system.file_name = file_name
        file_in_system.file_size = file_size
        file_in_system.file_type = file_type
        file_in_system.file_date = file_date
        file_in_system.file_hash = file_hash
        file_in_system.is_deleted = file_deleted

        file_in_system.save()

    except FileInSystem.MultipleObjectsReturned:
        pass


def find_files(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if match_file_pattern(file):
                yield os.path.join(root, file)


class Command(BaseCommand):
    help = "collect fastq and fastq.gz files from SOURCE_DATA_ROOT recursively"

    def handle(self, *args, **options):
        self.stdout.write(f"Collecting fastq files from {SOURCE_DATA_ROOT}")
        for file_path in find_files(SOURCE_DATA_ROOT):
            update_file_info(file_path)

        self.stdout.write(f"Collected fastq files from {SOURCE_DATA_ROOT}")
