# Generated by Django 4.2.5 on 2024-05-28 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process_files', '0002_rename_insaflaccount_insafluaccount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='televirsample',
            name='machine',
        ),
        migrations.RemoveField(
            model_name='televirsample',
            name='user',
        ),
        migrations.AddField(
            model_name='televirsample',
            name='account',
            field=models.ManyToManyField(to='process_files.insafluaccount'),
        ),
    ]
