from django.urls import path
from .views import *

app_name = 'Account'

urlpatterns = [
    path('subject/', SubjectView.as_view(), name='subjects'),
    path('<int:game_id>/problem/single/<int:single_problem_id>/',
         PlayerSingleProblemView.as_view(), name='one detailed problem'),
    path('<int:game_id>/problem/single/', SingleProblemView.as_view(), name='one problem'),
    path('<int:game_id>/problem/multiple/<int:multiple_problem_id>',
         PlayerMultipleProblemView.as_view(), name='one problem'),
    path('<int:game_id>/problem/multiple/', MultipleProblemView.as_view(), name='one problem'),
]
