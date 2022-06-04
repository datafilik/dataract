from django.contrib import admin

# Register your models here.
from .models import DataSet, TrainedMLModel

admin.site.register(DataSet)
admin.site.register(TrainedMLModel)
