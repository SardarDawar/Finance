
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView


# url patterns under ('')
urlpatterns = [
    # user/profile urls
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('admin-panel/', RedirectView.as_view(url='/admin'), name='admin-panel')
]