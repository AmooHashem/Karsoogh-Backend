from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import *

app_name = 'Account'

urlpatterns = [
    # Your URLs...
    path('create-user/', CreateUserAPI.as_view(), name='create user'),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordAPI.as_view(), name='change-password')
]
