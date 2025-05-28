from django.urls import path
from . import views

urlpatterns = [
    path('<int:problem_id>/', views.submit_code, name='submit_code'),
    path('history/', views.submission_history, name='submission_history'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
