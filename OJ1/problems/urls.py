from django.urls import path
from .views import problem_list, problem_detail

urlpatterns = [
    path('', problem_list, name='problem-list'),
    path('<int:pk>/', problem_detail, name='problem-detail'),
]
