from django.db import models

class Repository(models.Model):
    name = models.CharField(max_length=200, unique=True)
    path = models.CharField(max_length=255)
    type = models.IntegerField(default=0)
