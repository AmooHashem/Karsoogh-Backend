from django.urls import path
from .views import *

app_name = 'Account'

urlpatterns = [
    path('subject/', SubjectView.as_view(), name='subjects'),
    path('problem/single/', SingleProblemView.as_view(), name='one problem'),
    path('problem/multiple/', MultipleProblemView.as_view(), name='one problem'),
    path('problem/single/random/', GetRandomSingleProblem.as_view(), name='one problem'),
    path('problem/multiple/random/', GetRandomMultipleProblem.as_view(), name='one problem'),
]
