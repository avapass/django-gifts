from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=50)
    price = models.FloatField()
    description = models.CharField(max_length=100)
    image = models.FileField(null=True, blank=True)