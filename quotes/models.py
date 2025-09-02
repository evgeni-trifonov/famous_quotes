from django.db import models

# Create your models here.

# quotes/models.py
from django.db import models

class Quote(models.Model):
    text = models.TextField(unique=True)  # Ограничение "a": уникальность
    source = models.CharField(max_length=200)
    weight = models.IntegerField(default=1)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)  # Счётчик просмотров

    def __str__(self):
        return f'"{self.text[:50]}..." - {self.source}'

