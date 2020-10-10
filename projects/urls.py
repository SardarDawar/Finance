
from django.contrib import admin
from django.urls import path, re_path
from .views import ProjectList, project

# url patterns under ('projects/')
urlpatterns = [

    # projects urls
    path('', ProjectList.as_view(), name='projects'),
    path('<str:slug>/', project, name='project-detail'),
]
