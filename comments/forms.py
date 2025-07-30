# comments/forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'نظر خود را بنویسید...', 'rows': 3}),
        }



from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'content']
