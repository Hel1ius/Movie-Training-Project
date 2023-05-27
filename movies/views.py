from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Movie, Category
from .forms import ReviewForm


class MoviesView(ListView):
    model = Movie
    template_name = 'movies/movies.html'
    context_object_name = 'movie_list'

    def get_queryset(self):
        movie_list = super().get_queryset().filter(draft=False)
        return movie_list


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'
    slug_field = 'url'
    context_object_name = 'movie'


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
