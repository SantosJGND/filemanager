# Generated by Django 4.2.5 on 2024-06-21 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collect_files', '0010_systemsample_fastq_file_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemsample',
            name='nfiles',
            field=models.IntegerField(default=0),
        ),
    ]
