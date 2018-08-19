from articlesApp.models import Article
from django import forms


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('name', 'description', 'image', 'state' )
