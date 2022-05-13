from django.contrib import admin
from .models import Movie, Actor

# Register your models here.
admin.site.register(Actor)
admin.site.register(Movie)