import json
from random import choice

from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response

from Game.models import Subject, PlayerSingleProblem, PlayerMultipleProblem, Player, Problem, MultipleProblem, Game
from Game.serializers import SingleProblemSerializer, SubjectSerializer, MultipleProblemSerializer, \
    ProblemDetailedSerializer, MultipleProblemDetailedSerializer


class SubjectView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SubjectSerializer

    def post(self, request):
        game_id = request.data['game_id']
        queryset = Subject.objects.filter(game__id=game_id)
        serializer = self.get_serializer(data=queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data, status.HTTP_200_OK)


def get_random(query_set):
    pks = query_set.values_list('pk', flat=True).order_by('id')
    random_pk = choice(pks)
    return query_set.get(pk=random_pk)


class SingleProblemView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SingleProblemSerializer
    queryset = PlayerSingleProblem.objects.all()

    def get(self, request, game_id):
        user = request.user
        player = Player.objects.filter(game__id=game_id, user=user)
        query_set = self.get_queryset().filter(player=player)
        serializer = self.get_serializer(data=query_set, many=True)
        serializer.is_valid()
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, game_id):
        print(request.data)
        user, subject_id, difficulty = request.user, request.data['subject'], request.data['difficulty']
        if subject_id is None or difficulty is None:
            return Response({"message": "لطفاً تمام مشخصات خواسته‌شده را وارد کنید!"}, status.HTTP_404_NOT_FOUND)

        subject = Subject.objects.get(id=subject_id)
        player = Player.objects.get(game__id=game_id, user=user)
        player_single_problems = self.get_queryset().filter(player=player).values_list('problem', flat=True)
        available_problems = Problem.objects.filter(subject=subject, difficulty=difficulty) \
            .exclude(id__in=player_single_problems.all())
        if available_problems.count() == 0:
            return Response({"message": "شما تمام سوالات این بخش را گرفته‌اید!"}, status.HTTP_404_NOT_FOUND)

        selected_problem = get_random(available_problems)
        newPlayerSingleProblem = PlayerSingleProblem()
        newPlayerSingleProblem.player = player
        newPlayerSingleProblem.problem = selected_problem
        newPlayerSingleProblem.game = Game.objects.get(id=game_id)
        newPlayerSingleProblem.save()
        return Response({"message": "سوال دنباله‌دار با موفقیت اضافه شد!"}, status.HTTP_200_OK)


class MultipleProblemView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MultipleProblemSerializer
    queryset = PlayerMultipleProblem.objects.all()

    def get(self, request, game_id):
        user = request.user
        query_set = self.get_queryset().filter(player__user=user, game__id=game_id)
        serializer = self.get_serializer(data=query_set, many=True)
        serializer.is_valid()
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, game_id):
        user = request.user
        player = Player.objects.get(game__id=game_id, user=user)
        player_multiple_problems = self.get_queryset().filter(player=player).values_list('multiple_problem', flat=True)
        available_problems = MultipleProblem.objects.all().exclude(id__in=player_multiple_problems.all())
        if available_problems.count() == 0:
            return Response({"message": "شما تمام سوالات این بخش را گرفته‌اید!"}, status.HTTP_404_NOT_FOUND)

        selected_problem = get_random(available_problems)
        newPlayerMultipleProblem = PlayerMultipleProblem()
        newPlayerMultipleProblem.player = player
        newPlayerMultipleProblem.multiple_problem = selected_problem
        newPlayerMultipleProblem.game = Game.objects.get(id=game_id)
        newPlayerMultipleProblem.save()
        return Response({"message": "سوال دنباله‌دار با موفقیت اضافه شد!"}, status.HTTP_200_OK)
