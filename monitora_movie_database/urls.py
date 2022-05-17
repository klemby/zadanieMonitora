from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name='index'),
    path('movie/<int:id>', views.movie_view, name='movie'),
    path('actor/<int:id>', views.actor_view, name='actor'),
]