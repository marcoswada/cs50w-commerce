from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    description = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.description}"
    class Meta:
        verbose_name_plural="Categories"

class Listing(models.Model):
    active = models.BooleanField()
    owner = models.ForeignKey(User, on_delete=models.PROTECT,related_name='seller')
    creationDate = models.DateTimeField()
    title = models.CharField(max_length=70)
    picture = models.ImageField(upload_to="pictures", blank=True, null=True)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    initialPrice = models.DecimalField(max_digits=10, decimal_places=2)
    currentPrice = models.DecimalField(max_digits=10, decimal_places=2)
    watchedBy = models.ManyToManyField(User, blank=True)
    def __str__(self):
        return (f"({ self.id }) { self.title }")

class Bid(models.Model):
    bidDate = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Listing, on_delete=models.PROTECT)
    bidder = models.ForeignKey(User, on_delete=models.PROTECT)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return (f"{ self.bidDate } - { self.item.title } { self.bidder } { self.value }")

class Comment(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=255, blank=False, null=False)
    def __str__(self):
        return(f"({ self.id }) { self.item } { self.user }: { self.comment }")
