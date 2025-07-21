from django import forms
from .models import Email
from ckeditor.widgets import CKEditorWidget

class EmailForm(forms.ModelForm):
    متن = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Email
        fields = ['عنوان', 'متن']  # فقط فیلدهای قابل ویرایش را اینجا می‌ذاریم
        widgets = {
            'متن': forms.Textarea(attrs={'rows': 5, 'cols': 40}),  # به متن شکل textarea می‌دهد
        }
