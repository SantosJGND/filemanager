# Generated by Django 4.2.5 on 2023-09-26 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collect_files', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileinsystem',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
