from abc import ABC, abstractmethod
from typing import List, Literal

import pandas as pd
from collect_files.models import FileInSystem
from django.db.models import Q
from django.utils.timezone import make_aware
from collect_files.models import SystemSample, UpdateSystemSamples


class FastqDatabaseConnector(ABC):
    sample_col_name: str = "sample_name"
    filename_col_name: str = "filename"

    @abstractmethod
    def prep(self):
        pass

    @abstractmethod
    def query_filenames(self, sample_names: list[str]) -> pd.DataFrame:
        pass


class ExcelImport(FastqDatabaseConnector):
    engine: Literal["xlrd", "openpyxl", "odf", "pyxlsb"] | None = "openpyxl"
    panel: str = "Fastq_Database"
    filename_col_excel = "FASTQ FILE NAME"

    sample_name_col_excel = "Sample/Isolate/Strain Designation"
    simplified_sample_name_col_excel = "Sample Name (Simplified)"

    columns = [
        "Order",
        "Deparment/Unit",
        "Species",
        "Sample/Isolate/Strain Designation",
        "Interest (Surveillance; Reasearch; Tests)",
        "Project/Work Title",
        "Requester/Owner",
        "Published ID",
        "SRA/ENA",
        "Run Accession # (Fastq)",
        "Assembly Accession #",
        "BIOProject",
        "UTI-Seq Original ID",
        "NGS Instrument",
        "Read size",
        "UTI-SEQ Run #",
        "Run Date",
        "UTI RUN CODE",
        "Notes",
        "Outputs",
        "FASTQ FILE NAME",
        "Link to Location in Storage3par",
        "EXTERNAL DISK Location",
    ]

    def __init__(self, file):
        self.file = file
        try:
            self.sample_files_df = pd.DataFrame(
                columns=[self.sample_col_name, self.filename_col_name]
            )
        except Exception as e:
            print(e)
            raise ValueError("Error reading the file")

    def read_panels(self):
        return pd.read_excel(self.file, sheet_name=self.panel, engine=self.engine)

    def get_sample_filenames(self) -> pd.DataFrame:
        df = self.read_panels()

        return df[[self.sample_name_col_excel, self.filename_col_excel]].rename(
            columns={
                self.sample_name_col_excel: self.sample_col_name,
                self.filename_col_excel: self.filename_col_name,
            }
        )

    def prep(self):
        self.sample_files_df = (
            self.get_sample_filenames()
            .dropna(subset=[self.filename_col_name])
            .drop_duplicates(subset=[self.filename_col_name])
            .reset_index(drop=True)
        )

        self.sample_files_df[self.simplified_sample_name_col_excel] = (
            self.sample_files_df[self.sample_col_name].str.replace("-", "_")
        )

    def query_filenames(self, sample_names: list[str]) -> pd.DataFrame:
        """
        Query the sample files dataframe for a list of sample names.
        it is possible that the original name has a different combination of - and _.
        """

        return self.sample_files_df[
            self.sample_files_df[self.sample_col_name].isin(sample_names)
            | self.sample_files_df[self.simplified_sample_name_col_excel].isin(
                sample_names
            )
        ]


import re


def find_pattern_in_string(s):
    patterns = [
        r"_S\d+_R\d+_\d+\.fastq\.gz",
        r"_R\d+_\d+\.fastq\.gz",
        r"_S\d+_L\d+_R\d+_\d+\.fastq\.gz",
    ]
    all_matches = []
    for pattern in patterns:
        matches = re.findall(pattern, s)
        if matches:
            all_matches.extend(matches)
    return all_matches


##
class SystemConnector:
    """
    class to connect to the file system and query files
    """

    def __init__(self):
        pass

    def query_filepaths(self, file_names: list[str]):
        """
        Query the file system for a list of sample names.
        """
        files = FileInSystem.objects.filter(file_name__in=file_names)

        return files

    def query_files_by_filename(self, file_name: str) -> List[FileInSystem]:
        """
        Query the file system for a list of sample names.
        """

        file_names = file_name.split(";")

        files = FileInSystem.objects.filter(file_name__in=file_names)

        return files

    def query_files_by_filename_nosample(self, file_name: str) -> List[FileInSystem]:
        """
        Query the file system for a list of sample names.
        """

        file_names = file_name.split(";")

        files = FileInSystem.objects.filter(
            file_name__in=file_names, system_sample=None
        )

        return files

    @staticmethod
    def process_fastq_filenames(fastq_file_name: str):
        fastq_file_name_possibilities = fastq_file_name.split(";")
        all_possibilities = []
        print(fastq_file_name_possibilities)
        for filename in fastq_file_name_possibilities:
            # all_possibilities.append(filename.replace("-", "_"))
            # all_possibilities.append(filename.replace("_fastq", ".fastq.gz"))
            name = filename.replace("_R2.fastq.gz", "")
            name = name.replace("_R1.fastq.gz", "")
            pattern_found = find_pattern_in_string(name)
            if pattern_found:
                for pattern in pattern_found:
                    name = name.replace(pattern, "")
            collapsed = name + "_collapse"
            all_possibilities.append(collapsed)
            all_possibilities.append(name)
        print(all_possibilities)
        fastq_file_name_possibilities = list(set(all_possibilities))
        return fastq_file_name_possibilities

    def query_files_by_sample(self, sample: SystemSample) -> List[FileInSystem]:
        """
        Query the file system for a list of sample names.
        """

        fastq_file_name = sample.fastq_file_name
        fastq_file_name_possibilities = self.process_fastq_filenames(fastq_file_name)
        pk_list = []
        for filename in fastq_file_name_possibilities:
            files = FileInSystem.objects.filter(file_name__icontains=filename)
            if files.exists():
                # append all
                pk_list.extend(files.values_list("pk", flat=True))

        pk_list = list(set(pk_list))
        files = FileInSystem.objects.filter(pk__in=pk_list)
        # files = FileInSystem.objects.filter(file_name__in=fastq_file_name_possibilities)

        return files

    def query_filepath(self, row: pd.Series) -> str:
        """
        Query the file system for a list of sample names.
        """
        file_name = row["filename"]
        sample_name = row["sample_name"]

        files = self.query_files_by_filename(file_name)
        file_path = ""
        if files.exists():
            file_path = files.first().file_path

        return file_path


class StockManager:
    time_zone = "UTC"
    sample_column_fields = [
        "Order",
        "Deparment/Unit",
        "Species",
        "Sample/Isolate/Strain Designation",
        "Interest (Surveillance; Reasearch; Tests)",
        "Project/Work Title",
        "Requester/Owner",
        "Published ID",
        "SRA/ENA Run Accession # (Fastq)",
        "Run Accession # (Fastq)",
        "BIOProject",
        "NGS Instrument",
        "Read size",
        "Run Date",
        "Notes",
        "FASTQ FILE NAME",
        "Link to Location in Storage3par",
    ]

    data_connector: FastqDatabaseConnector
    system_connector: SystemConnector

    def __init__(self, data_connector):
        self.data_connector = data_connector
        self.system_connector = SystemConnector()

    def query_filenames(self, sample_names: list[str]) -> pd.DataFrame:
        return self.data_connector.query_filenames(sample_names)

    def query_filepaths(self, file_names: list[str]) -> pd.DataFrame:
        sample_file_df = self.query_filenames(file_names)
        sample_file_df["file_path"] = sample_file_df.apply(
            self.system_connector.query_filepath, axis=1
        )
        return sample_file_df

    def sample_register(self, row: pd.Series):

        updated = 0

        ## print a log if row index is divisible by 1000
        if row.name % 1000 == 0:
            print(f"Processing row {row.name}")

        date_run = row["Run Date"]
        if isinstance(date_run, pd.Timestamp):
            date_run = date_run.strftime("%Y-%m-%d")
            # set the date to the timezone
            date_run = make_aware(pd.Timestamp(date_run), timezone=self.time_zone)

        elif date_run in ["Missing", "n.a.", "missing", "", "N/A"]:
            date_run = None

        else:
            try:
                date_year = int(date_run)
                date_run = f"{date_year}-01-01"
                date_run = make_aware(pd.Timestamp(date_run), timezone=self.time_zone)
            except:
                date_run = None

        #####
        try:
            system_sample = SystemSample.objects.get(
                sample_name=row["Sample/Isolate/Strain Designation"],
                order=row["Order"],
            )
        except SystemSample.DoesNotExist:

            system_sample = SystemSample(
                sample_name=row["Sample/Isolate/Strain Designation"],
                order=row["Order"],
                owner=row["Requester/Owner"],
                species=row["Species"],
                project=row["Project/Work Title"],
                bioproject=row["BIOProject"],
                department=row["Deparment/Unit"],
                interest=row["Interest (Surveillance; Reasearch; Tests)"],
                ngs_instrument=row["NGS Instrument"],
                read_size=row["Read size"],
                run_date=date_run,
                run_date_str=row["Run Date"],
                published_id=row["Published ID"],
                accession_id=row["SRA/ENA Run Accession # (Fastq)"],
                storage_link=row["Link to Location in Storage3par"],
                fastq_file_name=row["FASTQ FILE NAME"],
                notes=row["Notes"],
            )

            system_sample.save()

        files = self.system_connector.query_files_by_sample(system_sample)

        for file in files:
            file.system_sample = system_sample
            file.save()

        updated = 1

        return updated

    def sample_register_all(self, sample_file_df: pd.DataFrame) -> int:

        # remove nans from fastq file name
        sample_file_df = sample_file_df.dropna(subset=["FASTQ FILE NAME"])
        print(f"## Registering {sample_file_df.shape[0]} samples ##")
        update = sample_file_df.apply(self.sample_register, axis=1)

        UpdateSystemSamples.objects.create(samples_updated=update.sum())
        return update.sum()
