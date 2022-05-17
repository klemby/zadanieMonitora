from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseServerError
from .models import Movie, Actor


def index_view(request):
    try:
        if len(request.GET) == 0 or request.GET.__str__().__contains__("['']"):
            search = ' <None> '
        else:
            search = request.GET.get('q')
        actors = [a for a in Actor.objects.filter(name__icontains=search)]
        movies = [m for m in Movie.objects.filter(title__icontains=search)]
        context = {
            'actor_list': actors,
            'movie_list': movies
        }
        return render(request, 'index.html', context)
    except Exception as e:
        return HttpResponseServerError(e)


def movie_view(request, id):
    try:
        movie = Movie.objects.get(pk=id)
        context = {
            'movie': movie,
            'cast': movie.cast.all()
        }
        return render(request, 'movie.html', context)
    except Movie.DoesNotExist:
        raise Http404('Movie does not exist')


def actor_view(request, id):
    try:
        a = Actor.objects.get(pk=id)
        movies = a.movies.all()
        context = {
            'movie_list': movies
        }
        return render(request, 'actor.html', context)
    except Actor.DoesNotExist:
        raise Http404('Actor does not exist')
