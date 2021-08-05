from django.urls import path
from .views import *

app_name = 'Account'
urlpatterns = [
    path('<int:game_id>/player/', PlayerView.as_view(), name='get player info'),
    path('<int:game_id>/subject/', SubjectView.as_view(), name='subjects'),
    path('<int:game_id>/problem/single/', SingleProblemView.as_view(), name='one problem'),
    path('<int:game_id>/problem/single/<int:problem_id>/',
         PlayerSingleProblemView.as_view(), name='one detailed problem'),
    path('<int:game_id>/problem/multiple/', MultipleProblemView.as_view(), name='one problem'),
    path('<int:game_id>/problem/multiple/<int:problem_id>/',
         PlayerMultipleProblemView.as_view(), name='one problem'),
]