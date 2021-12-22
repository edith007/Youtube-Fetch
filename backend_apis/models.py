from django.db import models

# Create your models here.


class Backend_apis(models.Model):
    api_key = models.TextField()
    name = models.CharField(max_length=100, blank=True, null=True)
