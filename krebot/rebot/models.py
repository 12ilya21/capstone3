from django.db import models
from django.contrib.auth.models import User

class RestaurantInfo1(models.Model):
    name_ko = models.CharField(max_length=255, null=False)
    name_en = models.CharField(max_length=255, null=False)
    name_ja = models.CharField(max_length=255, null=False)
    name_zh = models.CharField(max_length=255, null=False)
    image_ko = models.ImageField(null=False, blank=False)
    image_en = models.ImageField(null=False, blank=False)
    image_ja = models.ImageField(null=False, blank=False)
    image_zh = models.ImageField(null=False, blank=False)
    bookmark_count = models.IntegerField(default=0)
    latitude = models.FloatField(null=False, default = 0.0)
    longitude = models.FloatField(null=False, default = 0.0)

class Bookmark(models.Model):
    username = models.CharField(max_length=150)
    restaurant_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('username', 'restaurant_name')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=10, choices=[
        ('en', 'English'),
        ('ko', 'Korean'),
        ('zh', 'Chinese'),
        ('ja', 'Japanese')
    ], default='en')