from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import *

app_name = 'Account'

urlpatterns = [
    path('player/problem/', PlayerProblemView.as_view(), name='player problems'),
    path('subject/', SubjectView.as_view(), name='subjects'),
    path('problem/', SubjectView.as_view(), name='one problem'),
]
