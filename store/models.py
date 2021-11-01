import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self) -> str:
        return self.name

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
