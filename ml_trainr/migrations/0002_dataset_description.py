# Generated by Django 2.2.14 on 2020-08-05 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ml_trainr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='description',
            field=models.TextField(default=models.CharField(help_text='Enter name of training data set (e.g. Solar iradiaton data for West Africa)', max_length=200), help_text='Give a brief desccription of data set you are uploading'),
        ),
    ]
