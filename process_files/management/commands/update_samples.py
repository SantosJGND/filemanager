import argparse
import os

import pandas as pd
from django.core.management.base import BaseCommand
from django.utils import timezone
from process_files.modules.connect_utils import ExcelImport, StockManager


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
        excel_file = os.path.join(
            "process_files", "modules", "DDI_BIOINF_NGS_MANAGEMENT.xlsx"
        )

        excel_import = ExcelImport(excel_file)
        excel_import.prep()
        filepath = options["file"]

        stock_manager = StockManager(excel_import)
        panel_samples = excel_import.read_panels()

        nsamples_updated = stock_manager.sample_register_all(panel_samples)
        print(f"## Updated samples {nsamples_updated} ##")
