# movie_project/movie_app/admin.py
from django.contrib import admin
from .models import Category, Movie, Review, UserProfile

admin.site.register(Category)
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(UserProfile)
