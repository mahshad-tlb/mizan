from django import forms
from .models import Email
from ckeditor.widgets import CKEditorWidget

class EmailForm(forms.ModelForm):
    body = forms.CharField(label='متن', widget=CKEditorWidget(config_name='inline_style'))

    class Meta:
        model = Email
        fields = ['title', 'body']
        labels = {
            'title': 'عنوان',
        }
