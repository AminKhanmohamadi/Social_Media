from django import forms
from .models import Post, Comment


class PostCreatUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }



class PostSearchForm(forms.Form):
    search = forms.CharField()