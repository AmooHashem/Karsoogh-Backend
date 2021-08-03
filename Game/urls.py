from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import *

app_name = 'Account'

urlpatterns = [
    path('player/problem/', PlayerProblemView.as_view(), name='salam'),
    path('problem/subject/', SubjectView.as_view(), name='salam'),
]
