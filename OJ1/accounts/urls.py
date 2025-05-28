from django.urls import path, include
from accounts.views import register_user, login_user, logout_user, profile_view

urlpatterns = [
    path("register/", register_user, name="register-user"),
    path("login/", login_user, name="login-user"),
    path("logout/", logout_user, name="logout-user"),
    path('profile/', profile_view, name='profile'),
]