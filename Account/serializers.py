from rest_framework.serializers import ModelSerializer
from .models import *


# todo:
# TokenObtainPairSerializer

class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['phone_number'], **validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class StudentSerializer(ModelSerializer):
    pass
