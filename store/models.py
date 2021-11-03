import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=200)
    start_price = models.IntegerField()
    photo = models.ImageField()

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    photo = models.ImageField()
    rating = models.IntegerField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self) -> str:
        return self.name

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
