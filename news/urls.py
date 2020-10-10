
from django.contrib import admin
from django.urls import path
from .views import NewsList, news_article

# url patterns under ('news/')
urlpatterns = [

    # news urls
    path('', NewsList.as_view(), name='news'),
    path('<str:slug>/', news_article, name='news-detail'),
]
