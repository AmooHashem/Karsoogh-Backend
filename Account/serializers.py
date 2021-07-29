from rest_framework import serializers
from .models import *


# todo:
# TokenObtainPairSerializer

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class StudentSerializer(serializers.ModelSerializer):
    pass


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(max_length=250, required=True)
    new_password = serializers.CharField(max_length=250, required=True)

    def validated_password(self, value):
        validated_password(value)
        return value
