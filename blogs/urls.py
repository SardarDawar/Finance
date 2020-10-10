
from django.contrib import admin
from django.urls import path, re_path
from .views import BlogList, blog

# url patterns under ('blogs/')
urlpatterns = [

    # blogs urls
    path('', BlogList.as_view(), name='blogs'),
    path('<str:slug>/', blog, name='blog-detail'),
]
