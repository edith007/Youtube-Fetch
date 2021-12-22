from django.db import models
from django.db.models import indexes

# Create your models here.


class SearchResults(models.Model):
    ids = models.CharField(max_length=50)
    title = models.TextField()
    description = models.TextField()
    published_datetime = models.DateTimeField()
    thumbnail_url = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=["published_datetime"]),
            models.Index(fields=["ids"]),
        ]
