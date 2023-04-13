from .views import MovieView, MovieDetailView, MovieOrderDetailView
from django.urls import path
from rest_framework_simplejwt import views

urlpatterns = [
    path("movies/", MovieView.as_view()),
    path("movies/<int:movie_id>/", MovieDetailView.as_view()),
    path("movies/<int:movie_id>/orders/", MovieOrderDetailView.as_view()),
]
