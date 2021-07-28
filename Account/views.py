from django.shortcuts import render
from rest_framework import generics 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import *
from .models import User


# todo:
# GenericAPIView

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class CreateUserAPI(generics.ListCreateAPIView):
    
    def get_queryset(self):
        return User.objects.all()

    serializer_class = CreateUserSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response({"user": serializer.data})


class ChangePassWordAPI(generics.UpdateAPIView):
    serializer_class = ChangePassWordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    
    def put(self, request, *args, **kwargs):
        self.object = get_object()
        self.object = self.request.user
        serializer = self.get_serializer(data = request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_pass')):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_pass"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)