from django.shortcuts import render
from collect_files.tables import FileInSystemTable, SystemSampleTable
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from .models import FileInSystem, SystemSample
from typing import Any
from django_tables2 import RequestConfig
from django.db.models import Q
from filemanager.forms import UploadFileForm
# this is to remove
import pandas as pd

class FilesView(generic.ListView):
    template_name = "collect_files/file_index.html"
    context_object_name = "file_list"
    paginate_by = 10

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        files_in_system = FileInSystem.objects.all()

        # Get the search term from the request
        search_term = self.request.GET.get("search", "")

        # Filter the files based on the search term
        if search_term:
            files_in_system = files_in_system.filter(
                Q(file_name__icontains=search_term)
                | Q(file_path__icontains=search_term)
                | Q(system_sample__sample_name__icontains=search_term)
            )

        files_table = FileInSystemTable(files_in_system)

        # Apply pagination
        page_number = kwargs.get("page", 1)
        files_table.paginate(per_page=25)
        # paginator = Paginator(files_table, 10)  # Show 10 rows per page
        RequestConfig(self.request, paginate={"per_page": 25}).configure(files_table)

        context["files_table"] = files_table
        context["search_term"] = search_term

        return context

    def get_queryset(self):
        return FileInSystem.objects.all()


# generic.CreateView <- This one handles post...
class UploadIndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "collect_files/upload.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # This one is not handling post...
        if self.request.method == 'POST':
            form = UploadFileForm(self.request.POST, self.request.FILES)
            if form.is_valid():
                form.save()
                
                uploaded_file = self.request.FILES['file']
                ##RequestExcelImport(uploaded_file)
                #context['success'] = uploaded_file
                context['success'] = "This part is never run..."

                return context
        else:
            form = UploadFileForm()
            context['form'] = form

        return context
    
    def post(self,request):
        my_data = request.POST
        # do something with your data
        context = {}  #  set your context

        form = UploadFileForm(request.POST, self.request.FILES)
        if form.is_valid():
            form.filename = self.request.FILES['file'] 
            form.save()


        #context['success'] = self.request.FILES['file'] 
        ##RequestExcelImport(uploaded_file)
        results = pd.read_excel(self.request.FILES['file'],
                                sheet_name="Folha1", 
                                skiprows=range(10),
                                engine="openpyxl")

        context['success'] = results.loc[0].iat[1]
        #return super(generic.TemplateView, self).render_to_response(context)
        return self.render_to_response(context)
    
# generic.CreateView <- This one handles post...
class ValidateSamplesView(LoginRequiredMixin, generic.TemplateView):
    template_name = "collect_files/validate.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # This one is not handling post...
        if self.request.method == 'POST':
            form = UploadFileForm(self.request.POST, self.request.FILES)
            if form.is_valid():
                form.save()
                
                uploaded_file = self.request.FILES['file']
                ##RequestExcelImport(uploaded_file)
                #context['success'] = uploaded_file
                context['success'] = "This part is never run..."

                return context
        else:
            form = UploadFileForm()
            context['form'] = form

        return context
    
    def post(self,request):
        my_data = request.POST
        # do something with your data
        context = {}  #  set your context

        form = UploadFileForm(request.POST, self.request.FILES)
        if form.is_valid():
            form.filename = self.request.FILES['file'] 
            form.save()


        #context['success'] = self.request.FILES['file'] 
        ##RequestExcelImport(uploaded_file)
        results = pd.read_excel(self.request.FILES['file'],
                                sheet_name="Folha1", 
                                skiprows=range(10),
                                engine="openpyxl")

        context['success'] = results.loc[0].iat[1]
        #return super(generic.TemplateView, self).render_to_response(context)
        return self.render_to_response(context)
    
# generic.CreateView <- This one handles post...
class GenerateRunView(LoginRequiredMixin, generic.TemplateView):
    template_name = "collect_files/generate_run.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # This one is not handling post...
        if self.request.method == 'POST':
            form = UploadFileForm(self.request.POST, self.request.FILES)
            if form.is_valid():
                form.save()
                
                uploaded_file = self.request.FILES['file']
                ##RequestExcelImport(uploaded_file)
                #context['success'] = uploaded_file
                context['success'] = "This part is never run..."

                return context
        else:
            form = UploadFileForm()
            context['form'] = form

        return context
    
    def post(self,request):
        my_data = request.POST
        # do something with your data
        context = {}  #  set your context

        form = UploadFileForm(request.POST, self.request.FILES)
        if form.is_valid():
            form.filename = self.request.FILES['file'] 
            form.save()


        #context['success'] = self.request.FILES['file'] 
        ##RequestExcelImport(uploaded_file)
        results = pd.read_excel(self.request.FILES['file'],
                                sheet_name="Folha1", 
                                skiprows=range(10),
                                engine="openpyxl")

        context['success'] = results.loc[0].iat[1]
        #return super(generic.TemplateView, self).render_to_response(context)
        return self.render_to_response(context)

class SamplesView(generic.TemplateView):
    template_name = "collect_files/sample_index.html"
    #context_object_name = "sample_list"
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        samples_in_system = SystemSample.objects.all()

        # Get the search term from the request
        search_term = self.request.GET.get("search", "")

        # Filter the files based on the search term
        if search_term:
            samples_in_system = samples_in_system.filter(
                Q(sample_name__icontains=search_term)
                | Q(species__icontains=search_term)
                | Q(project__icontains=search_term)
                | Q(bioproject__icontains=search_term)
            )

        # sort by date earliest to latest
        samples_in_system = samples_in_system.order_by("-run_date")

        samples_table = SystemSampleTable(samples_in_system)

        # Apply pagination
        samples_table.paginate(per_page=25)
        # paginator = Paginator(files_table, 10)  # Show 10 rows per page
        RequestConfig(self.request, paginate={"per_page": 25}).configure(samples_table)

        context["samples_table"] = samples_table
        context["search_term"] = search_term

        return context

    def get_queryset(self):
        return SystemSample.objects.all()
