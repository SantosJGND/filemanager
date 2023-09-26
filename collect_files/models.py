from django.db import models

# Create your models here.


class FileInSystem(models.Model):

    file_name = models.CharField(max_length=200)
    file_path = models.FilePathField(path="/", max_length=200)
    file_size = models.IntegerField()
    file_type = models.CharField(max_length=200)
    file_date = models.DateTimeField('date published')
    file_hash = models.CharField(max_length=200)

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.file_name