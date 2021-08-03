from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response

from Game.models import PlayerProblem, Subject
from Game.serializers import PlayerProblemSerializer, SubjectSerializer


class PlayerProblemView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PlayerProblemSerializer

    def get(self, request):
        user = request.user
        query_set = PlayerProblem.objects.filter(player__user=user)
        serializer = self.get_serializer(data=query_set, many=True)
        serializer.is_valid()
        return Response(serializer.data, status.HTTP_200_OK)


class SubjectView(generics.GenericAPIView):
    queryset = Subject.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = SubjectSerializer

    def get(self, request):
        serializer = self.get_serializer(data=self.get_queryset(), many=True)
        serializer.is_valid()
        return Response(serializer.data, status.HTTP_200_OK)


class GetRandomProblem(generics.GenericAPIView):
    queryset = Subject.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = SubjectSerializer
