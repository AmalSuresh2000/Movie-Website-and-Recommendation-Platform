from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import UserProfileForm, MovieForm, ReviewForm, CustomUserCreationForm
from .models import Movie, Review, Category

def home(request):
    movie_list = Movie.objects.all()
    paginator = Paginator(movie_list, 8)

    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)

    context = {'movies': movies}
    return render(request, 'home.html', context)

def movie_details(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    reviews = Review.objects.filter(movie=movie)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been added successfully.')
            return redirect('movie_details', movie_id=movie_id)
    else:
        form = ReviewForm()

    return render(request, 'movie_details.html', {'movie': movie, 'reviews': reviews, 'form': form})

@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movie added successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Failed to add movie. Please correct the errors below.')
    else:
        form = MovieForm()
    return render(request, 'add_movie.html', {'form': form})

@login_required
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_details', movie_id=movie_id)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'edit_movie.html', {'form': form})

@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        movie.delete()
        return redirect('home')
    return render(request, 'delete_movie.html', {'movie': movie})

def category_movies(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    movies = Movie.objects.filter(category=category)
    return render(request, 'category_movies.html', {'category': category, 'movies': movies})

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        review.review = request.POST.get('review')
        review.rating = request.POST.get('rating')
        review.save()
        return redirect('movie_details', movie_id=review.movie.id)
    return render(request, 'edit_review.html', {'review': review})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    movie_id = review.movie.id
    review.delete()
    return redirect('movie_details', movie_id=movie_id)

def search_movies(request):
    query = request.GET.get('q')
    movies = Movie.objects.filter(title__icontains=query) if query else []
    return render(request, 'search_results.html', {'movies': movies, 'query': query})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

@login_required
def update_profile(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect(reverse('profile'))
        else:
            messages.error(request, 'There was an error updating your profile. Please correct the errors below.')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'update_profile.html', {'form': form})
