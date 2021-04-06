from django.urls import path
from Formula0 import views

app_name = 'Formula0'

urlpatterns = [
    path('student/login/', views.login, name='login'),
    path('student/get_team_data/', views.get_team_data, name='login'),

    path('student/request_problem/', views.request_problem, name='request_problem'),
    # path('student/submit_answer/<int:id>/', views.request_problem, name='request_problem'),

    path('student/get_auction_problems/', views.get_auction_problems, name='get_auction_problems'),
    path('student/put_problem_in_auction/', views.put_problem_in_auction, name='put_problem_in_auction'),
    path('student/get_problem_from_auction/', views.get_problem_from_auction,
         name='get_problem_from_auction'),

    path('student/get_problem/', views.get_problem, name='get_problem'),
    path('student/get_problems/', views.get_problems, name='get_problems'),

    # path('mentor/get_uncorrected_problems/', views.get_uncorrected_problems, name='get_uncorrected_problems'),
    # path('mentor/submit_problem_score/', views.submit_problem_score, name='submit_problem_score'),
]
