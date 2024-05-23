from django.urls import path
from collect_files.views import FilesView, UploadIndexView, SamplesView, ValidateSamplesView, GenerateRunView

urlpatterns = [
    path("files/", FilesView.as_view(), name="manage"),
    path("files/", FilesView.as_view(), name="manage_files"),
    path("upload_user_request/", UploadIndexView.as_view(), name="upload_user_request"),
    path("validate_samples/", ValidateSamplesView.as_view(), name="validate_samples"),
    path("generate_run/", GenerateRunView.as_view(), name="generate_run"),    
    path("samples/", SamplesView.as_view(), name="samples"),
]
# Path: collect_files/views.py
