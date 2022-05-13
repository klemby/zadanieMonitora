import requests
from bs4 import BeautifulSoup
from collections import namedtuple
from zadanieMonitora.wsgi import *
from monitora_movie_database.models import Actor, Movie

Movie_namedtuple = namedtuple('Movie', ['title', 'url'])


class CSFDscrapper():
    def __init__(self, mainURL='https://www.csfd.cz', toplistURL='https://www.csfd.cz/zebricky/filmy/nejlepsi/?from='):
        self.MAIN_URL = mainURL
        self.TOP_LIST_URL = toplistURL
        self.HEADERS = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
        self.ACTOR_MARK = 'Hrají: '
        self.movies = []

    def __create_top_movies_list(self, final_count, movies_list=None, pagination=0):
        self.movies = [] if movies_list is None else movies_list
        if final_count - len(self.movies) <= 0:
            return
        soup = BeautifulSoup(requests.get(self.TOP_LIST_URL + str(pagination), headers=self.HEADERS).text,
                             'html.parser')
        self.movies.extend([Movie_namedtuple(a.findNext('a', attrs={'class': 'film-title-name'})['title'],
                                  a.findNext('a', attrs={'class': 'film-title-name'})['href']) for a in
                            soup.find_all('div', attrs={'class': 'article-content'})[:final_count - len(self.movies)]])
        pagination += 100
        self.__create_top_movies_list(movies_list=self.movies, final_count=final_count, pagination=pagination)

    def get_cast(self, movieurl):
        soup = BeautifulSoup(requests.get(self.MAIN_URL + movieurl, headers=self.HEADERS).text, 'html.parser')
        creators = soup.find('div', attrs={'class': 'creators'})
        cast = creators.find('h4', text=self.ACTOR_MARK).parent
        return [actor.getText() for actor in cast.find_all('a')]


    def get_top_movies(self, number):
        self.__create_top_movies_list(final_count=number)
        return self.movies


    def load_db(self, number_of_movies):
        self.get_top_movies(number_of_movies)
        for movie in self.movies:
            if Movie.objects.filter(title=movie.title).count() == 0:
                print(f"Loading movie {movie.title}")
                m = Movie(title=movie.title)
                m.save()
                cast = self.get_cast(movie.url)
                for a in cast:
                    if Actor.objects.filter(name=a).count() == 0:
                        ac = Actor(name=a)
                        ac.save()
                        ac.movies.add(m)
                    else:
                        ac = Actor.objects.filter(name=a)[0]
                        ac.movies.add(m)
            else:
                print(f'Skipping {movie.title}')
                pass
