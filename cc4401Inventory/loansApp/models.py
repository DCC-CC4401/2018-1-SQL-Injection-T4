from mainApp.models import Action
from articlesApp.models import Article
from django.db import models


class Loan(Action):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Préstamos"
        ordering = ['pk']