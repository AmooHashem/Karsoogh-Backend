from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from models import *

# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(
#         write_only=True,
#         required=True,
#         help_text='Leave empty if no change needed',
#         style={'input_type': 'password', 'placeholder': 'Password'}
#     )
#
#     def create(self, validated_data):
#         validated_data['password'] = make_password(validated_data.get('password'))
#         return super(UserSerializer, self).create(validated_data)
#
#     class Meta:
#         model = User
#         fields = ['email', 'username', 'phone_number', 'password']
