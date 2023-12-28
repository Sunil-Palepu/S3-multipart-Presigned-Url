from django.db import models

# Create your models here.
class MyModel(models.Model):
    object_path = models.CharField(max_length=255)
