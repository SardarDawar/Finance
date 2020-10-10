import os
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from common.storage import OverwriteStorage
from common.utils import resizeImage

CUST_BASE_PATH = 'customers'
CUST_PROFILE_PICTURES_PATH = os.path.join(CUST_BASE_PATH, 'profile_pictures')
CUST_DEFAULT_PROFILE_IMAGE_PATH = os.path.join(CUST_BASE_PATH, 'default_profile_picture.png')

DASHIMG_BASE_PATH = 'dashboard'

def custProfileImageSavePath(instance, filename):
    return os.path.join(CUST_PROFILE_PICTURES_PATH, f'{slugify(instance.name)}_{slugify(instance.profession)}'+os.path.splitext(filename)[1])

class CustomerReview(models.Model):
    name = models.CharField(max_length=50)
    profession = models.CharField(max_length=100)
    image = models.ImageField(default=CUST_DEFAULT_PROFILE_IMAGE_PATH, storage=OverwriteStorage(), upload_to=custProfileImageSavePath)    
    review_quote = models.TextField()
    # extra
    dt_creation = models.DateTimeField(default=timezone.now)
    dt_review = models.DateField(default=timezone.now)
    
    class Meta:
        ordering = ['-dt_review']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)        
        # resize image
        resizeImage(self.image.path, 300, 300)

    def __str__(self):
        return f'{self.name} ({self.profession}) - [{self.dt_review}]'

class DashboardImage(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to=DASHIMG_BASE_PATH)    
    dt_creation = models.DateTimeField(default=timezone.now)
    dt_show = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['dt_show']

    def __str__(self):
        if self.name: 
            return f'Dashboard Image ({self.name}) - [{self.dt_show}]'
        else:
            return f'Dashboard Image ({self.image.name}) - [{self.dt_show}]'

class CustomerMessage(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=150)
    message = models.TextField()
    dt_creation = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-dt_creation']

    def __str__(self):
        return f'Message from ({self.name}) ({self.subject}) - [{self.dt_creation}]'