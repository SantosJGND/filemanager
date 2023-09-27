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
        parser.add_argument(
            "-o",
            "--output",
            help="Output file name",
            default="matched_samples.tsv",
        )

    def handle(self, *args, **options):
        excel_file = os.path.join(
            "process_files", "modules", "DDI_BIOINF_NGS_MANAGEMENT.xlsx"
        )

        excel_import = ExcelImport(excel_file)
        excel_import.prep()
        filepath = options["file"]
        output = options["output"]
        query_file = pd.read_csv(filepath, sep="\t")
        sample_names = query_file["sample_name"].unique().tolist()

        stock_manager = StockManager(excel_import)
        samples_df = stock_manager.query_filepaths(sample_names)

        print("## Matched samples ##")
        print(samples_df.shape[0])
        print(samples_df.head())

        samples_df.to_csv(output, sep="\t", index=False)
