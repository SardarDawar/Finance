
from django.contrib import admin
from django.urls import path, re_path
from .views import (home, about, solutions, contact, privacy, 
                    createComment_AJAX, createReply_AJAX, deleteComment_AJAX, deleteReply_AJAX, sendMessage_AJAX,
                    newsletterSubscribe_AJAX, newsletterUnsubscribe, schedule_meeting)

# url patterns under ('')
urlpatterns = [

    # base site urls
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('solutions/', solutions, name='solutions'),
    path('contact/', contact, name='contact'),
    path('privacy/', privacy, name='privacy'),
    path('schedule-meeting/', schedule_meeting, name='schedule-meeting'),

    # api urls
    path('api/comments/create/', createComment_AJAX, name='create-comment'),
    path('api/comments/delete/', deleteComment_AJAX, name='delete-comment'),
    path('api/replies/create/', createReply_AJAX, name='create-reply'),
    path('api/replies/delete/', deleteReply_AJAX, name='delete-reply'),
    path('api/message/', sendMessage_AJAX, name='send-message'),
    path('api/newsletter/subscribe/', newsletterSubscribe_AJAX, name='newsletter-subscribe'),
    path('api/newsletter/unsubscribe/<uidb64>/<token>/', newsletterUnsubscribe, name='newsletter-unsubscribe'),
]
