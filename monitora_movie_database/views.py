from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Movie, Actor
from django.template import loader
# Create your views here.

def index(request):
    try:
        print(len(request.GET))
        if len(request.GET) == 0 or request.GET.__str__().__repr__().__contains__("['']"):
            print('nahradene')
            search = ' <None> '
        else:
            search = request.GET.get('q')
        if len(search) > 0:
            actors = [a for a in Actor.objects.filter(name__icontains=search)]
            movies = [m for m in Movie.objects.filter(title__icontains=search)]
            template = loader.get_template('index.html')
            context = {
                'actor_list': actors,
                'movie_list': movies
            }
        else:
            raise
        return HttpResponse(template.render(context, request))
    except Exception as e:
        return e


def movie(request, id):
    try:
        movie = Movie.objects.get(pk=id)
        cast = movie.cast.all()
        template = loader.get_template('movie.html')
        context = {
            'movie': movie,
            'cast': cast
        }
        return HttpResponse(template.render(context, request))
    except Movie.DoesNotExist:
        raise Http404('Movie does not exist')


def actor(request, id):
    try:
        a = Actor.objects.get(pk=id)
        movies = a.movies.all()
        template = loader.get_template('actor.html')
        context = {
            'movie_list': movies
        }
        return HttpResponse(template.render(context, request))
    except Actor.DoesNotExist:
        raise Http404('Actor does not exist')
