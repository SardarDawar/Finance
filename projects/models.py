from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from common.utils import resizeImage
import os

BASE_PATH = 'projects'
PROJECT_IMAGES_PATH = os.path.join(BASE_PATH, 'images')
PROJECT_DOWNLOADS_PATH = os.path.join(BASE_PATH, 'files')
DEFAULT_PROJECT_IMAGE_PATH = os.path.join(BASE_PATH, 'default_image.jpg')

def projectImageSavePath(instance, filename):
    return os.path.join(PROJECT_IMAGES_PATH, f'{slugify(instance.title)}'+os.path.splitext(filename)[1])

def projectDownloadsSavePath(instance, filename):
    return os.path.join(PROJECT_DOWNLOADS_PATH, f'{slugify(instance.title)}'+os.path.splitext(filename)[1])

class Project(models.Model):
    # creator
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="projects")
    # main
    ptype = models.CharField(max_length=50, default='PROJECT')
    title = models.CharField(max_length=100)
    image = models.ImageField(default=DEFAULT_PROJECT_IMAGE_PATH, upload_to=projectImageSavePath)
    detail = models.TextField()
    # about
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    dt_creation = models.DateTimeField(default=timezone.now)
    dt_project = models.DateField(default=timezone.now)
    # extra
    demo_url = models.URLField(max_length=250, blank=True, null=True)
    download_file = models.FileField(null=True, blank=True, upload_to=projectDownloadsSavePath)
    
    class Meta:
        ordering = ['-dt_project']

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
        return f'{self.title} ({self.ptype}) - [{self.dt_project}]'