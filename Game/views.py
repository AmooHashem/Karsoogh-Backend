from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response

from Game.models import Subject, PlayerSingleProblem, PlayerMultipleProblem
from Game.serializers import SingleProblemSerializer, SubjectSerializer, MultipleProblemSerializer


class SubjectView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SubjectSerializer

    def post(self, request):
        game_id = request.data['game_id']
        queryset = Subject.objects.filter(game__id=game_id)
        serializer = self.get_serializer(data=queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data, status.HTTP_200_OK)


class SingleProblemView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SingleProblemSerializer
    queryset = PlayerSingleProblem.objects.all()

    def post(self, request):
        game_id = request.data['game_id']
        user = request.user
        query_set = self.get_queryset().filter(player__user=user, game__id=game_id)
        serializer = self.get_serializer(data=query_set, many=True)
        serializer.is_valid()
        return Response(serializer.data, status.HTTP_200_OK)


class MultipleProblemView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MultipleProblemSerializer
    queryset = PlayerMultipleProblem.objects.all()

    def post(self, request):
        game_id = request.data['game_id']
        user = request.user
        query_set = self.get_queryset().filter(player__user=user, game__id=game_id)
        serializer = self.get_serializer(data=query_set, many=True)
        serializer.is_valid()
        return Response(serializer.data, status.HTTP_200_OK)


class GetRandomSingleProblem(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SubjectSerializer

    def post(self, request):
        user = request.user


class GetRandomMultipleProblem(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SubjectSerializer
