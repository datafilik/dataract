from django.shortcuts import render

# Create your views here.

from ml_trainr.models import DataSet
from ml_trainr.models import TrainedMLModel
from ml_trainr.forms import UploadDatasetForm
from django.http import HttpResponseRedirect

# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.neural_network import MLPClassifier

# import tensorflow as tf
# import numpy as np
# import pandas as pd
# from tensorflow import keras
# from tensorflow.keras import layers

import h2o
from h2o.automl import H2OAutoML


def index(request):
    #View function for home page of site.

    # Generate counts of some of the main objects
    num_dataset = DataSet.objects.all().count()
    # num_ml_models = TrainedMLModel.all().count()

    # Generate form for uploading data
    if request.method == 'POST':
       
        # Get the posted form
        dset_upld_form = UploadDatasetForm(request.POST, request.FILES)

        dset_upld_form.save()  # save file.
            
    else:

        dset_upld_form = UploadDatasetForm()

    context = {
        'num_dataset': num_dataset,
        # 'num_ml_models': num_ml_models,
        'form': dset_upld_form,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def upload(request):

    # Generate counts of some of the main objects
    num_dataset = DataSet.objects.all().count()
    # num_ml_models = TrainedMLModel.all().count()

    # Generate form for uploading data
    if request.method == 'POST':
        # Get the posted form
        dset_upld_form = UploadDatasetForm(request.POST, request.FILES)

        # Get handle to database
        upld_dset = DataSet()
        ml_model = TrainedMLModel()

        if dset_upld_form.is_valid():

            # Collect data from posted form
            upld_dset.name = dset_upld_form.cleaned_data['name']
            upld_dset.description = dset_upld_form.cleaned_data['description']
            upld_dset.data_file = dset_upld_form.cleaned_data['data_file']
            upld_dset.resp_colmn = dset_upld_form.cleaned_data['response_column']
            # upld_dset.upload_date = dset_upld_form.cleaned_data['upload_date']

            # Push form data to database
            upld_dset.save()

            # Train ML model

            # AUTO ML TRAINING
            h2o.init()

            # Import a sample binary outcome train/test set into H2O
            data_file_path = 'uploads/' + str(dset_upld_form.cleaned_data['data_file'])
            data_frame = h2o.import_file(data_file_path)

            # Identify predictors/features and response/
            x = data_frame.columns
            y = upld_dset.resp_colmn
            x.remove(y)

            # split input data into into Train/Test/Validation. Here training data has 70% and validation data 15%
            train_frame, test_frame, validn_frame = data_frame.split_frame(ratios=[0.7, 0.15], seed=1)

            # Run AutoML for 20 base models (limited to 1 hour max runtime by default if max_runtime_secs not specfied)
            aml_model = H2OAutoML(max_models=20, seed=1, max_runtime_secs=600)
            aml_model.train(x=x, y=y, training_frame=train_frame)

            # save model as in binary format
            # model_path = h2o.save_model(model=aml_model, path="/tmp/mymodel", force=True)
            
            # load the model
            # saved_model = h2o.load_model(model_path)

            # get the leader model
            leadr_model = aml_model.leader

            # test trained model
            #pred_response = aml_model.predict(test_frame)
            #OR
            pred_response = leadr_model.predict(test_frame)

            # get model performance. see https://docs.h2o.ai/h2o/latest-stable/h2o-docs/performance-and-prediction.html
            #perf_data = leadr_model.*

            # save model as in binary format
            model_path = h2o.save_model(
                model=leadr_model, path="trained_models/", force=True)

            # download the model built above to your local machine
            # ml_model.model_file = h2o.download_model(aml_model)
            ml_model.model_file = str(model_path)

            # specifies model name and description based on same from uploaded data set
            ml_model.name = upld_dset.name

            ml_model.description = upld_dset.description

            # MANUAL ML TRAINING
            # load data
            # data_frame = pd.read_csv(upld_dset.data_file) 

            # split data
            # y = data_frame.temp
            # x = data_frame.drop('temp', axis=1)

            # x_train, x_test, y_train, y_test = train_test_split(
            #     x, y, test_size=0.2)

            # clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
            #         hidden_layer_sizes=(5, 2), random_state=1)

            # clf.fit(x_train, y_train)


            # Push trained ml model data to database
            ml_model.save()

    else:

        dset_upld_form = UploadDatasetForm()

    context = {
        'num_dataset': num_dataset,
        # 'num_ml_models': num_ml_models,
        'form': dset_upld_form,
    }
    # change url to ML training outcome page. locals()
    return render(request, 'index.html', context=context)
