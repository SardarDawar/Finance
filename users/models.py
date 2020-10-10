import os
from django.contrib.auth.models import User
from django.db import models
from common.storage import OverwriteStorage
from common.utils import resizeImage

BASE_PATH = "users"
PROFILE_PICTURES_PATH = os.path.join(BASE_PATH, 'profile_pictures')
DEFAULT_PROFILE_IMAGE_PATH = os.path.join(BASE_PATH, 'default_profile_picture.png')

def profileImageSavePath(instance, filename):
    return os.path.join(PROFILE_PICTURES_PATH, f'{instance.user.username}'+os.path.splitext(filename)[1])

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=250, blank=True, null=True)
    image = models.ImageField(default=DEFAULT_PROFILE_IMAGE_PATH, storage=OverwriteStorage(), upload_to=profileImageSavePath)

    def __str__(self):
        return f'{self.user.username} - Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        resizeImage(self.image.path, 300, 300)
