from django.urls import path
from collect_files.views import FilesView, UploadIndexView

urlpatterns = [
    path("files/", FilesView.as_view(), name="manage"),
    path("files/page/<int:page>/", FilesView.as_view(), name="manage_files"),
    path("upload/", UploadIndexView.as_view(), name="upload"),
]
# Path: collect_files/views.py
