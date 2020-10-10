from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from common.utils import resizeImage
import os

BASE_PATH = 'blogs'
BLOG_IMAGES_PATH = os.path.join(BASE_PATH, 'images')
DEFAULT_BLOG_IMAGE_PATH = os.path.join(BASE_PATH, 'default_image.jpg')

def blogImageSavePath(instance, filename):
    return os.path.join(BLOG_IMAGES_PATH, f'{slugify(instance.title)}'+os.path.splitext(filename)[1])

class Blog(models.Model):
    # creator
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="blogs")
    # main
    title = models.CharField(max_length=100)
    image = models.ImageField(default=DEFAULT_BLOG_IMAGE_PATH, upload_to=blogImageSavePath)
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
        return f'{self.title} ({self.author.username}) - [{self.dt_creation}]'

class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="comments")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=500)
    dt_creation = models.DateTimeField(default=timezone.now)
    # non-user comment
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['dt_creation']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)        
        if self.user:
            if self.user.first_name and self.user.first_name:
                self.name = f'{self.user.first_name} {self.user.last_name}'
            elif self.user.first_name:
                self.name = self.user.first_name
            elif self.user.last_name:
                self.name = self.user.last_name
            else:
                self.name = self.user.username
            if self.user.email:
                self.email = self.user.email
        super().save(update_fields=['name', 'email'])

    def __str__(self):
        return f'Comment on ({self.blog.title}) by ({self.name}) - [{self.dt_creation}]'

class Reply(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="replies")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies")
    content = models.CharField(max_length=500)
    dt_creation = models.DateTimeField(default=timezone.now)
    # non-user comment
    name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['dt_creation']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)        
        if self.user:
            if self.user.first_name and self.user.first_name:
                self.name = f'{self.user.first_name} {self.user.last_name}'
            elif self.user.first_name:
                self.name = self.user.first_name
            elif self.user.last_name:
                self.name = self.user.last_name
            else:
                self.name = self.user.username
        super().save(update_fields=['name'])

    def __str__(self):
        return f'Reply on ({self.comment.blog.title}) by ({self.name}) - [{self.dt_creation}]'