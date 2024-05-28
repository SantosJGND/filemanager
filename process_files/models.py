from django.db import models

# Create your models here.


class InsafluMachine(models.Model):
    url = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    version = models.CharField(max_length=100)
    deprecated = models.BooleanField(default=False)


class InsafluAccount(models.Model):
    name = models.CharField(max_length=100)
    machine = models.ForeignKey(InsafluMachine, on_delete=models.CASCADE)


class InsafluProject(models.Model):
    name = models.CharField(max_length=100)
    account = models.ForeignKey(InsafluAccount, on_delete=models.CASCADE)
    url = models.CharField(max_length=100, default="")


class TelevirSample(models.Model):
    project = models.ManyToManyField(InsafluProject)
    account = models.ForeignKey(InsafluAccount, on_delete=models.CASCADE, default=None)
    sample_name = models.CharField(max_length=100)
    file_r1 = models.CharField(max_length=100)
    file_r2 = models.CharField(max_length=100)
