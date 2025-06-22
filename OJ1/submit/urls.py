from django.urls import path
from . import views
#from .views import ai_review

urlpatterns = [
    path('<int:problem_id>/', views.submit_code, name='submit_code'),
    path('history/', views.submission_history, name='submission_history'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('ai-review/', views.ai_review, name='ai_review'),
    path('run-code/', views.run_code_ajax, name='run_code_ajax'),
]
