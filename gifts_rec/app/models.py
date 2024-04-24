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

class Questionnaire(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

class Question(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='questions', blank=True)
    text = models.CharField(max_length=50)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', blank=True)
    text = models.CharField(max_length=50)
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.text

class UserProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'product')

class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friends_with')

    class Meta:
        unique_together = ('user', 'friend')

