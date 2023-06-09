from django.contrib.auth.models import AbstractUser
from django.db import models


def get_profile_image(self, file_name):
    return f'images/profile_images/{self.username}.jpg'


class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(
        upload_to=get_profile_image,
        max_length=255,
        default='images/profile_images/Default.png'
    )
    description = models.CharField(max_length=500, blank=True, null=True)

    followings = models.ManyToManyField('self', blank=True, related_name='user_followings', symmetrical=False)
    followers = models.ManyToManyField('self', blank=True, related_name='user_followers', symmetrical=False)

    def __str__(self):
        return self.username


