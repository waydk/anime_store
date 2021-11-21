import datetime

from django.db import models
from django.utils import timezone


class Categories(models.Model):
    name = models.CharField(max_length=200)
    start_price = models.IntegerField()
    photo = models.ImageField()

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    features = models.JSONField()
    price = models.IntegerField()
    photo = models.ImageField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self) -> str:
        return self.name

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Comments(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)
    author = models.CharField(max_length=200)
    on_moderation = models.BooleanField()
    pub_date = models.DateTimeField('date puplished')

    def __str__(self) -> str:
        return self.content

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class RatingStar(models.Model):
    value = models.SmallIntegerField(default='0')

    def __str__(self) -> str:
        return str(self.value)

    class Meta:
        ordering = ['-value']

class Rating(models.Model):
    user = models.CharField(max_length=200)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.star} - {self.product}"

class ShopCart(models.Model):
    user = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"{self.product.name}"


class Favorite(models.Model):
    user = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"{self.product.name}"
