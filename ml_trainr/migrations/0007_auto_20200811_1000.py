# Generated by Django 2.2.14 on 2020-08-11 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ml_trainr', '0006_trainedmlmodels'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TrainedMLModels',
            new_name='TrainedMLModel',
        ),
    ]
