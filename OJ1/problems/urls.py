from django.urls import path
from .views import problem_list, problem_detail
from . import views
urlpatterns = [
    path('', problem_list, name='problem-list'),
    path('<int:pk>/', problem_detail, name='problem-detail'),
    path('add/', views.add_problem, name='add_problem'),
    path('<int:pk>/edit/', views.edit_problem, name='edit_problem'),
]
