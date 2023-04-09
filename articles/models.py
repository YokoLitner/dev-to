from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
import os

# Create your models here.


class ArticleAbstract(models.Model):
    title = models.CharField()
    description = models.CharField()
    content = models.JSONField(null=True)
    url = models.URLField()
    published_at = models.TimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Article(ArticleAbstract):
    visible = models.BooleanField(default=True)


class ArticlesLatest(ArticleAbstract):
    reading_time_minutes = models.IntegerField()
    published_at = models.CharField()
    body_html = models.CharField(null=True)


class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=20)
    following = ArrayField(models.IntegerField(), null=True)
    articles = models.ManyToManyField(Article)
