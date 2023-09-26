from abc import ABC, abstractmethod
from typing import List, Literal

import pandas as pd
from collect_files.models import FileInSystem


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

        self.sample_files_df = pd.DataFrame(
            columns=[self.sample_col_name, self.filename_col_name]
        )

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

    def query_filenames(self, sample_names: list[str]) -> pd.DataFrame:
        """
        Query the sample files dataframe for a list of sample names.
        """
        return self.sample_files_df[
            self.sample_files_df[self.sample_col_name].isin(sample_names)
        ]


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

    def query_filepath(self, file_name: str):
        """
        Query the file system for a list of sample names.
        """
        try:
            file = FileInSystem.objects.get(file_name=file_name)
            file_path = file.file_path
        except FileInSystem.DoesNotExist:
            file_path = None
        except FileInSystem.MultipleObjectsReturned:
            files = FileInSystem.objects.filter(file_name=file_name).first()
            file_path = files.file_path

        return file_path


class StockManager:
    data_connector: FastqDatabaseConnector
    system_connector: SystemConnector

    def __init__(self, data_connector):
        self.data_connector = data_connector
        self.system_connector = SystemConnector()

    def query_filenames(self, sample_names: list[str]) -> pd.DataFrame:
        return self.data_connector.query_filenames(sample_names)

    def query_filepaths(self, file_names: list[str]) -> pd.DataFrame:
        sample_file_df = self.query_filenames(file_names)
        sample_file_df["file_path"] = sample_file_df["filename"].apply(
            self.system_connector.query_filepath
        )
        return sample_file_df
