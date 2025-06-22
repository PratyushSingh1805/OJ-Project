from django.urls import path, include
from accounts.views import register_user, login_user, logout_user, profile_view
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("register/", register_user, name="register-user"),
    path("login/", login_user, name="login-user"),
    path("logout/", logout_user, name="logout-user"),
    path('profile/', profile_view, name='profile'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
