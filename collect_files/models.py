from django.db import models

# Create your models here.


class UpdateSystemFiles(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    files_updated = models.IntegerField()


class SystemSample(models.Model):
    sample_name = models.CharField(max_length=200)
    order = models.IntegerField()
    project = models.CharField(max_length=200, default="")
    bioproject = models.CharField(max_length=200, default="")
    owner = models.CharField(max_length=200, default="")
    department = models.CharField(max_length=200, default="")
    species = models.CharField(max_length=200, default="")
    interest = models.CharField(max_length=200, default="")
    ngs_instrument = models.CharField(max_length=200, default="")
    read_size = models.CharField(max_length=200, default="")
    run_date = models.DateField(null=True, blank=True)
    run_date_str = models.CharField(max_length=200, default="")
    published_id = models.CharField(max_length=200, default="")
    accession_id = models.CharField(max_length=200, default="")
    storage_link = models.CharField(max_length=200, default="")
    notes = models.TextField(default="")

    @property
    def files(self):
        return FileInSystem.objects.filter(system_sample=self)


class UpdateSystemSamples(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    samples_updated = models.IntegerField()


class FileInSystem(models.Model):
    file_name = models.CharField(max_length=200)
    file_path = models.FilePathField(path="/", max_length=200)
    file_size = models.IntegerField()
    file_type = models.CharField(max_length=200)
    file_date = models.DateTimeField("date published")
    file_hash = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)

    system_sample = models.ForeignKey(
        SystemSample, on_delete=models.CASCADE, default=None, null=True
    )

    def __str__(self):
        return self.file_name
