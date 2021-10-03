from django.core import paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators .http import require_safe, require_POST, require_http_methods
from .models import Movie
from .forms import MovieForm
from django.core.paginator import Paginator


# 전체 목록 조회 페이지 반환
@require_safe
def index(request):
    movies = Movie.objects.order_by('-pk')
    paginator = Paginator(movies, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'movies': movies,
        'page_obj': page_obj,
    }
    return render(request, 'movies/index.html', context)


# POST 요청시 데이터 생성 및 Detail Page로 Redirect, 그 외에는 생성페이지 반환
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm()
        navbar = 'create'
    context = {
        'form': form,
        'navbar': navbar,
    }
    return render(request, 'movies/create.html', context)


# 상세페이지 반환
@require_safe
def detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    context = {
        'movie': movie,
    }
    return render(request, 'movies/detail.html', context)


# POST 요청시 데이터 수정 및 Detail Page로 Redirect, 그 외에는 수정페이지 반환
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            movie = form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm(instance=movie)
    context = {
        'form': form,
        'movie': movie,
    }
    return render(request, 'movies/update.html', context)


# POST 요청시 데이터 삭제 후 index Page로 Redirect
@require_POST
def delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    movie.delete()
    return redirect('movies:index')
