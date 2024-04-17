from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=50, unique=True)
    price = models.FloatField(db_index=True)
    description = models.CharField(max_length=150, null=True, blank=True, help_text="Add a description for this product")
    image = models.FileField(null=True, blank=True)
    favourite = models.ManyToManyField(User, related_name='favourite', blank=True)

    def __str__(self):
        return f"Product {self.title}"

    def get_absolute_url(self):
        return reverse_lazy("product-page", args=(self.id,))