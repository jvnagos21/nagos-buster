from django.urls import path
from .views import UserView
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import LoginView

urlpatterns = [
    path("users/", UserView.as_view()),
    path("users/login/", TokenObtainPairView.as_view()),
]
