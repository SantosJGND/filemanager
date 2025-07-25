import argparse
import os

import pandas as pd
from django.core.management.base import BaseCommand
from django.utils import timezone
from process_files.modules.connect_utils import ExcelImport, StockManager
from collect_files.models import UpdateSystemSamples


class Command(BaseCommand):
    """
    Django command to collect fastq files from the file system.
    """

    help = "Find samples in the file system"

    def add_arguments(self, parser):
        parser.add_argument(
            "-f",
            "--file",
            help="File to match: sample names, 1 per row, column = 'sample_name'",
            required=True,
        )

    def handle(self, *args, **options):
        filepath = options["file"]
        excel_file = os.path.join(filepath)
        self.stdout.write(f"Using Excel file: {excel_file}")
        excel_import = ExcelImport(excel_file)
        excel_import.prep()

        stock_manager = StockManager(excel_import)
        panel_samples = excel_import.read_panels()
        self.stdout.write(f"Found {len(panel_samples)} panel samples")
        self.stdout.write("## Matched samples ##")
        nsamples_updated = stock_manager.sample_register_all(panel_samples)
        print(f"## Updated samples {nsamples_updated} ##")
        
        UpdateSystemSamples.objects.create(samples_updated=nsamples_updated)
