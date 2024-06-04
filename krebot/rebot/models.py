from django.db import models

class RestaurantInfo1(models.Model):
    name = models.CharField(max_length=255, null=False)
    bookmark_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/')
    latitude = models.FloatField(null=False, default =0.0)
    longitude = models.FloatField(null=False, default =0.0)

class Bookmark(models.Model):
    username = models.CharField(max_length=150)
    restaurant_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('username', 'restaurant_name')
