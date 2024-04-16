from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=50)
    price = models.FloatField(db_index=True)
    description = models.CharField(max_length=150, null=True, blank=True, help_text="Add a description for this product")
    image = models.FileField(null=True, blank=True)

    def __str__(self):
        return f"Product {self.title}"