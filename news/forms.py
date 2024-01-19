# forms.py
from django import forms
from .models import Comment,News,Category

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body' , 'rating']

class PostForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title' , 'content', 'category' , 'writter','image']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        exclude = ['slug']