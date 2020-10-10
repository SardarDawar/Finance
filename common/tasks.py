from background_task import background
from background_task.models import Task, CompletedTask
from django.utils import timezone
from datetime import date, timedelta
from blogs.models import Blog
from news.models import NewsArticle, NewsletterSubscriber
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .tokens import emailVerificationToken
from django.contrib.sites.models import Site
from .utils import send_html_mail, get_seconds_until_next_weekday_hour_minute
from financehouse.glob_params import NEWSLETTER_MAILING_DAY, NEWSLETTER_MAILING_HOUR, NEWSLETTER_MAILING_MINUTE, NEWSLETTER_MAILING_FREQUENCY_MULTIPLIER
from datetime import datetime

MAX_NEWSLETTER_ARTICLES_COUNT = 3
MAX_NEWSLETTER_BLOGS_COUNT = 2

# newsletter worker

@background(schedule=timezone.now())
def check_send_newsletters():
    Task.objects.all().delete()
    CompletedTask.objects.all().delete()
    articles = NewsArticle.objects.filter(dt_creation__gte=(date.today() - timedelta(days=7))).order_by('-dt_creation')[:MAX_NEWSLETTER_ARTICLES_COUNT]
    blogs = Blog.objects.filter(dt_creation__gte=(date.today() - timedelta(days=7))).order_by('-dt_creation')[:MAX_NEWSLETTER_BLOGS_COUNT]
    if articles.count() > 0 or blogs.count() > 0:
        send_newsletters(articles, blogs)

def send_newsletters(articles, blogs):
    for sub in NewsletterSubscriber.objects.all():
        html_message = render_to_string('news/newsletter.html', {
            'name': sub.email.split("@")[0],
            'email': sub.email,
            'domain': Site.objects.get_current().domain,
            'articles': articles,
            'blogs': blogs,
            'todays_date': datetime.today(),
            'uid':urlsafe_base64_encode(force_bytes(sub.pk)),
            'token':emailVerificationToken.make_token(sub),
        }) 
        subject = f'{Site.objects.get_current().domain} Newsletter'
        send_html_mail(subject, html_message, [sub.email])

def schedule_newsletter():
    Task.objects.all().delete()
    CompletedTask.objects.all().delete()
    sched_eta_seconds = get_seconds_until_next_weekday_hour_minute(NEWSLETTER_MAILING_DAY, NEWSLETTER_MAILING_HOUR, NEWSLETTER_MAILING_MINUTE)
    repeat_seconds = get_repeat_seconds(NEWSLETTER_MAILING_FREQUENCY_MULTIPLIER)
    check_send_newsletters(schedule=sched_eta_seconds, repeat=repeat_seconds)

def get_repeat_seconds(multiplier):
    if multiplier == 0.5:
        return int(Task.WEEKLY*abs(0.5))
    if multiplier == 2:
        return Task.EVERY_2_WEEKS
    if multiplier == 4:
        return Task.EVERY_4_WEEKS 
    return Task.WEEKLY

