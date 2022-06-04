from django import forms
from django.utils import timezone
import datetime
    
class UploadDatasetForm(forms.Form):

    data_file = forms.FileField(help_text='Click the Browse button above to upload your dataset')

    name = forms.CharField(
        max_length=200, help_text='Enter name of training data set (e.g. Solar iradiaton data for West Africa)')

    response_column = forms.CharField(max_length=200,
        help_text="Enter name of reponse column in data set or make sure a column in your data set is called 'response'")

    description = forms.CharField(
        widget=forms.Textarea, help_text='Give a brief description of data set you are uploading')
    

    # cur_time = timezone.now()
    # upload_date = forms.DateTimeField(widget=forms.HiddenInput(
    #     attrs={'value': cur_time}), input_formats=['%m/%d/%y %H:%M'])
    #upload_date.widget.attrs.update('value'=cur_time)
