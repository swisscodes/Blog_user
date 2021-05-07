from django import forms
from .models import Comment, Post
from django.contrib.admin.widgets import AdminSplitDateTime


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "email", "body")


class SearchForm(forms.Form):
    query = forms.CharField()


class UserPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "image", "body", "status", "tags")
