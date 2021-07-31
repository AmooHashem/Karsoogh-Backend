from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import *

app_name = 'Account'

urlpatterns = [
    path('account/create/', CreateUserAPI.as_view(), name='create user'),
    path('account/login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('account/login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('account/change-password/', ChangePasswordAPI.as_view(), name='change-password'),
    path('account/reset-password/', ResetPasswordAPI.as_view(), name='reset-password'),
]
