# Generated by Django 4.1.7 on 2023-03-06 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0003_remove_dataschema_status_datasets'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DataSets',
            new_name='DataSet',
        ),
    ]
