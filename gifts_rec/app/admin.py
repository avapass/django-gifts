from django.contrib import admin
from .models import Product, Question, Answer, Questionnaire

# Register your models here.

admin.site.register(Product)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Questionnaire)