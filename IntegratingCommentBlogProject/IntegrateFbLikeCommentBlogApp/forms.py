from django import forms
from .models import Comment
class EmailSendForm(forms.Form):
    name=forms.CharField()
    sender=forms.EmailField()
    to=forms.EmailField()
    comments=forms.CharField(widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=("comment_body",)
