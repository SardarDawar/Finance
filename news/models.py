from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from common.utils import resizeImage
import os

BASE_PATH = 'news'
NEWS_IMAGES_PATH = os.path.join(BASE_PATH, 'images')
DEFAULT_NEWS_IMAGE_PATH = os.path.join(BASE_PATH, 'default_image.jpg')

def newsImageSavePath(instance, filename):
    return os.path.join(NEWS_IMAGES_PATH, f'{slugify(instance.title)}'+os.path.splitext(filename)[1])

class NewsArticle(models.Model):
    # creator
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="news_articles")
    # main
    title = models.CharField(max_length=100)
    image = models.ImageField(default=DEFAULT_NEWS_IMAGE_PATH, upload_to=newsImageSavePath)
    content = models.TextField()
    # about
    slug = models.SlugField(max_length = 250, null=True, blank=True)
    dt_creation = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-dt_creation']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)        
        # set post slug
        self.slug = self.get_slug()
        # resize image
        resizeImage(self.image.path, 850, 850)
        super().save(update_fields=['slug'])

    def get_slug(self):
        return f'{slugify(self.title)}-{self.id}'

    def __str__(self):
        if self.author:
            return f'{self.title} ({self.author.username}) - [{self.dt_creation}]'
        else:
            return f'{self.title} - [{self.dt_creation}]'


class NewsletterSubscriber(models.Model):
    email = models.EmailField(max_length=100)
    dt_added = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-dt_added']

    def __str__(self):
        return f'Newsletter Subscriber ({self.email}) - [{self.dt_added}]'