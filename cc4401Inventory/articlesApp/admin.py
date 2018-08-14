from django.contrib import admin
from .models import Article


class ArticleAdministrator(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'state')


admin.site.register(Article, ArticleAdministrator)
