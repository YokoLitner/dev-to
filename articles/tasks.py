import requests
from django.conf import settings
import json
from articles.models import ArticlesLatest
from dataclasses import dataclass
from celery import shared_task


@dataclass
class ArticleDTO:
    id: int
    title: str
    description: str
    url: str
    published_at: str
    reading_time_minutes: str


def handle_article_response(resp) -> list[ArticleDTO]:
    data = resp.json()
    articles = [ArticleDTO(item["id"], item["title"], item["description"],
                           settings.APP_URL+'/article/'+str(item["id"]), item["published_at"], item["reading_time_minutes"]) for item in data]
    return articles


def get_res_settings():
    JSON_HEADERS = {
        'Content-Type': "application/json",
        'Accept': "application/json"
    }
    body = json.dumps({
        'key': 'val'
    })

    return {'headers': JSON_HEADERS,
            'body': body}


def get_articles():
    res_settings = get_res_settings()
    response = requests.get(settings.API_BASE_URL +
                            '/latest', headers=res_settings['headers'], json=res_settings['body'])
    articles = handle_article_response(response)

    try:
        [ArticlesLatest(**article.__dict__).save()
         for article in articles]
        [get_article_content(article.__dict__['id']) for article in articles]
        print('get_articles: success')
    except Exception as e:
        print(f'get_articles: error: {e}')


def get_article_content(id: int):
    res_settings = get_res_settings()
    response = requests.get(settings.API_BASE_URL +
                            '/' + str(id), headers=res_settings['headers'], json=res_settings['body'])

    article = ArticlesLatest.objects.get(id=id)
    article.body_html = response.json()['body_html']
    status = article.save()
    print(str(id) + ' content updating:' +
          ('error', 'success')[status == None])


@shared_task
def load_articles():
    ArticlesLatest.objects.all().delete()
    get_articles()
