from django.urls import path
from collect_files.views import (
    download_tsv,
    FilesView,
    UploadIndexView,
    SamplesView,
    download_csv_for_FileInSystem,
)

urlpatterns = [
    path("files/", FilesView.as_view(), name="manage"),
    path("files/", FilesView.as_view(), name="manage_files"),
    path("upload/", UploadIndexView.as_view(), name="upload"),
    path("samples/", SamplesView.as_view(), name="samples"),
    path("download_tsv/", download_tsv, name="download_tsv"),
    path(
        "download_tsv_fileinsystem/",
        download_csv_for_FileInSystem,
        name="download_tsv_fileinsystem",
    ),
]
# Path: collect_files/views.py
