"""
URL configuration for filemanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path  # new

from process_files import views

urlpatterns = [
    # Your other URL patterns...
    path("create_machine/", views.create_insaflu_machine, name="create_machine"),
    path("deprecate_machine/", views.deprecate_machine, name="deprecate_machine"),
    path("get_machines/", views.get_machines, name="get_machines"),
    path("add_account/", views.add_account, name="add_account"),
    path("get_accounts/", views.get_insaflu_accounts, name="get_accounts"),
    path("metagenomics/", views.MetagenomicsView.as_view(), name="metagenomics"),
    path("upload_samples/", views.upload_samples, name="upload_samples"),
    path("get_samples/", views.get_televir_samples, name="get_samples"),
]
