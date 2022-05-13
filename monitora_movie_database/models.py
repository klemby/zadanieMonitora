from django.db import models


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Actor(models.Model):
    name = models.CharField(max_length=200, default='')
    movies = models.ManyToManyField(Movie, related_name='cast')

    def __str__(self):
        return self.name
