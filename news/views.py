from django.shortcuts import render
from .models import NewsArticle
from django.http import Http404
from django.core.paginator import Paginator
from django.views.generic import ListView

LATEST_NEWS_ARTICLES_COUNT = 3
ARTICLES_PER_PAGE = 6

class NewsList(ListView):
    model = NewsArticle
    paginate_by = ARTICLES_PER_PAGE
    template_name = 'news/news.html'
    context_object_name = 'news'
    ordering = ['-dt_creation']    

def news_article(request, slug):
    try:
        article = NewsArticle.objects.get(slug__iexact=slug)
    except NewsArticle.DoesNotExist:
        raise Http404(f"Blog does not exist.")
    latest_news_articles = NewsArticle.objects.all()[:LATEST_NEWS_ARTICLES_COUNT]
    context = {
        'article': article,
        'latest_news_articles': latest_news_articles,
    }
    return render(request, 'news/article.html', context)