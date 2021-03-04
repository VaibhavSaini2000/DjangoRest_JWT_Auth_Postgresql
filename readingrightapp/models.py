from django.db import models

# Create your models here.
class Post(models.Model):
    userId = models.IntegerField()
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=500)