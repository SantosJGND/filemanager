from django.urls import path
from collect_files.views import FilesView, UploadIndexView, SamplesView

urlpatterns = [
    path("files/", FilesView.as_view(), name="manage"),
    path("files/", FilesView.as_view(), name="manage_files"),
    path("upload/", UploadIndexView.as_view(), name="upload"),
    path("samples/", SamplesView.as_view(), name="samples"),
]
# Path: collect_files/views.py
