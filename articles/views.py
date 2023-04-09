from django.shortcuts import render, redirect
from articles.forms import ArticleForm
from articles.models import ArticlesLatest


def index(request):
    articles = ArticlesLatest.objects.all()[:30]
    return render(request, 'index.html', {'articles': articles})


def article(request, id):
    article = ArticlesLatest.objects.get(id=id)
    return render(request, 'article.html', {'article': article})
