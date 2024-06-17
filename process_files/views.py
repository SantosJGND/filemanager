from typing import Any
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from process_files.models import InsafluMachine
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import InsafluMachine, InsafluProject, InsafluAccount, TelevirSample
import pandas as pd


@require_POST
def create_insaflu_machine(request):
    url = request.POST.get("url")
    description = request.POST.get("description")
    version = request.POST.get("version")

    # Validate the data here as needed...
    if InsafluMachine.objects.filter(url=url).exists():
        # Redirect to an error page or something
        return redirect("home")

    # Create a new InsafluMachine object
    machine = InsafluMachine(url=url, description=description, version=version)
    machine.save()

    # Redirect to the home page (or wherever you want)
    return redirect("home")


@require_POST
def add_account(request):

    if request.method == "POST":
        name = request.POST.get("name")
        machine_id = request.POST.get("machine_id")
        machine = InsafluMachine.objects.get(id=machine_id)
        account = InsafluAccount(name=name, machine=machine)
        account.save()
        return JsonResponse({"status": "success"})


@require_POST
def deprecate_machine(request):

    if request.method == "POST":
        id = request.POST.get("machine_id")
        machine = InsafluMachine.objects.get(id=id)
        machine.deprecated = True
        machine.save()
        return JsonResponse({"status": "success"})


def get_machines(request):
    machines = InsafluMachine.objects.filter(deprecated=False)
    return JsonResponse(
        {
            "machines": [
                {
                    "id": machine.id,
                    "url": machine.url,
                    "description": machine.description,
                    "version": machine.version,
                }
                for machine in machines
            ]
        },
    )


#####################################################################
#####################################################################
from django.views import generic


class MetagenomicsView(generic.TemplateView):

    template_name = "process_files/metagenomics_main.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = {}

        return context


@require_GET
def get_televir_samples(request):
    samples = TelevirSample.objects.all()
    return JsonResponse(
        {
            "samples": [
                {
                    "id": sample.id,
                    "name": sample.sample_name,
                    "file_r1": sample.file_r1,
                    "file_r2": sample.file_r2,
                    "projects": ", ".join(
                        [project.name for project in sample.project.all()]
                    ),
                    "account": sample.account.name,
                    "machine": sample.account.machine.url,
                }
                for sample in samples
            ]
        }
    )


@require_GET
def get_insaflu_accounts(request):

    def process_machine_url(url: str):
        return (
            url.replace("http://", "")
            .replace("https://", "")
            .replace(":8000", "")
            .replace(":8000/", "")
        )

    def account_name(account: InsafluAccount):
        return f"{account.name} ({process_machine_url(account.machine.url)})"

    try:
        accounts = InsafluAccount.objects.filter(machine__deprecated=False)

        return JsonResponse(
            {
                "accounts": [
                    {"id": account.id, "name": account_name(account)}
                    for account in accounts
                ]
            }
        )

    except Exception as e:
        print(e)
        return JsonResponse({"accounts": []})


@csrf_exempt
@require_POST
def upload_samples(request):
    if request.method == "POST":

        try:
            file = request.FILES["file"]

            df = pd.read_csv(file, sep="\t")

        except Exception as e:
            print(e)
            return JsonResponse(
                {"message": "Error uploading file", "is_ok": False, "empty": True}
            )

        try:

            # get project urls
            project_url = request.POST.get("url")
            project_name = request.POST.get("name")
            account_id = int(request.POST.get("account"))
            account = InsafluAccount.objects.get(id=account_id)

            if project_name is not None:
                try:
                    project = InsafluProject.objects.get(
                        name=project_name, account=account
                    )
                    project.url = project_url
                except InsafluProject.DoesNotExist:
                    project = InsafluProject(
                        name=project_name, url=project_url, account=account
                    )

                project.save()

            for row in df.iterrows():
                row = row[1]
                try:
                    sample = TelevirSample.objects.get(sample_name=row["sample name"])
                    sample.file_r1 = row["fastq1"]
                    sample.file_r2 = row["fastq2"]
                    sample.account = account
                    sample.save()
                except TelevirSample.DoesNotExist:

                    sample = TelevirSample(
                        sample_name=row["sample name"],
                        file_r1=row["fastq1"],
                        file_r2=row["fastq2"],
                        account=account,
                    )
                    sample.save()

                if project_name is not None:
                    sample.project.add(project)

            # Do something with the DataFrame
            return JsonResponse(
                {"message": "File uploaded", "is_ok": True, "empty": False}
            )
        except Exception as e:
            print(e)
            return JsonResponse(
                {"message": "Error uploading file", "is_ok": False, "empty": False}
            )

    return JsonResponse({"message": "Method not allowed"})
