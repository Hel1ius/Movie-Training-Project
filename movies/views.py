from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.http import HttpResponse

from .models import Movie, Actor, Genre, Rating
from .forms import ReviewForm, RatingForm


class GenreYear():
    # Выводим Жанры и года
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values('year')


class MoviesView(GenreYear, ListView):
    model = Movie
    template_name = 'movies/movies.html'
    context_object_name = 'movie_list'
    paginate_by = 1

    def get_queryset(self):
        movie_list = super().get_queryset().filter(draft=False)
        return movie_list


class MovieDetailView(GenreYear, DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'
    slug_field = 'url'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        context['form'] = ReviewForm()
        return context


class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(DetailView):
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'


class SearchMoviesView(ListView):
    template_name = 'movies/movies.html'

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = f'q={self.request.GET.get("q")}&'
        return context


class FilterMoviesView(GenreYear, ListView):
    template_name = 'movies/movies.html'
    paginate_by = 1

    # Делаем фильтрацию фильмов
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(draft=False),
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres__in=self.request.GET.getlist('genre'))
        ).distinct()
        return queryset


class AddStarRating(View):
    # ip пользователя
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get('movie')),
                defaults={'star_id': int(request.POST.get('star'))}
            )
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponse(status=400)
