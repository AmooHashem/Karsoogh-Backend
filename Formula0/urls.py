from django.urls import path
from Formula0 import views

app_name = 'Formula0'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('get_problem/', views.get_problem_of_subject, name='login'),
    path('submit_problem/', views.get_problem_of_subject, name='login'),
    path('auction/get_problem/', views.get_problem_of_subject, name='login'),
    path('auction/submit_problem/', views.get_problem_of_subject, name='login'),
    path('scoreboard/', views.get_problem_of_subject, name='login'),

]
