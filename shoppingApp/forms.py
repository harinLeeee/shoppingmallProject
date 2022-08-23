from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        #fields = '__all__'
        fields = ['title', 'body', 'photo']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class SearchForm(forms.Form):
    search = forms.CharField(label='찾으시는 상품을 검색하세요 ', max_length=100)