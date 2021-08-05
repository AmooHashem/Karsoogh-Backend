from random import choice

from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response

from Game.models import Subject, PlayerSingleProblem, PlayerMultipleProblem, Player, Problem, MultipleProblem, Game, \
    Transaction
from Game.serializers import SingleProblemSerializer, SubjectSerializer, MultipleProblemSerializer, \
    ProblemDetailedSerializer, PlayerSingleProblemDetailedSerializer


class SubjectView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SubjectSerializer

    def get(self, request, game_id):
        queryset = Subject.objects.filter(game__id=game_id)
        serializer = self.get_serializer(data=queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data, status.HTTP_200_OK)


class PlayerSingleProblemView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PlayerSingleProblemDetailedSerializer
    queryset = PlayerSingleProblem.objects.all()

    def get(self, request, game_id, single_problem_id):
        user = request.user
        player = Player.objects.get(game__id=game_id, user=user)
        player_single_problem_query_set = self.get_queryset() \
            .filter(player=player, problem__id=single_problem_id)
        if player_single_problem_query_set.count() == 0:
            return Response({"message": "شما دسترسی ندارید!"}, status.HTTP_403_FORBIDDEN)
        player_single_problem = player_single_problem_query_set.first()
        player_single_problem_serializer = self.get_serializer(player_single_problem)
        return Response(player_single_problem_serializer.data, status.HTTP_200_OK)


class PlayerMultipleProblemView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProblemDetailedSerializer
    queryset = PlayerMultipleProblem.objects.all()

    def get(self, request, game_id, multiple_problem_id):
        user = request.user
        player = Player.objects.get(game__id=game_id, user=user)
        player_multiple_problem_query_set = self.get_queryset() \
            .filter(player=player, multiple_problem_id=multiple_problem_id)
        if player_multiple_problem_query_set.count() == 0:
            return Response({"message": "شما دسترسی ندارید!"}, status.HTTP_403_FORBIDDEN)
        player_multiple_problem = player_multiple_problem_query_set.first()
        single_problem = player_multiple_problem.multiple_problem.problems.all()[player_multiple_problem.step]
        single_problem_serializer = self.get_serializer(single_problem)
        return Response(single_problem_serializer.data, status.HTTP_200_OK)

    def post(self, request, game_id, multiple_problem_id):
        answer = request.data.answer
        user = request.user
        player = Player.objects.get(game__id=game_id, user=user)
        player_multiple_problem_query_set = self.get_queryset() \
            .filter(player=player, multiple_problem_id=multiple_problem_id)
        if player_multiple_problem_query_set.count() == 0:
            return Response({"message": "شما دسترسی ندارید!"}, status.HTTP_403_FORBIDDEN)
        player_multiple_problem = player_multiple_problem_query_set.first()
        single_problem = player_multiple_problem.multiple_problem.problems.all()[player_multiple_problem.step]
        # single_problem  |||| answer


class SingleProblemView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SingleProblemSerializer
    queryset = PlayerSingleProblem.objects.all()

    def get(self, request, game_id):
        user = request.user
        player = Player.objects.get(game__id=game_id, user=user)
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
        print(player_single_problems, difficulty)

        available_problems = Problem.objects.filter(subject=subject, difficulty=difficulty, type='DESCRIPTIVE') \
            .exclude(id__in=player_single_problems.all())
        if available_problems.count() == 0:
            return Response({"message": "شما تمام سوالات این بخش را گرفته‌اید!"}, status.HTTP_404_NOT_FOUND)

        selected_problem = get_random(available_problems)
        newPlayerSingleProblem = PlayerSingleProblem()
        newPlayerSingleProblem.player = player
        newPlayerSingleProblem.problem = selected_problem
        newPlayerSingleProblem.game = Game.objects.get(id=game_id)
        newPlayerSingleProblem.save()
        # todo: make transaction
        return Response({"message": "سوال تکی با موفقیت اضافه شد!"}, status.HTTP_200_OK)


class MultipleProblemView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MultipleProblemSerializer
    queryset = PlayerMultipleProblem.objects.all()

    def get(self, request, game_id):
        user = request.user
        player = Player.objects.get(game__id=game_id, user=user)
        query_set = self.get_queryset().filter(player=player)
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
        # todo: make transaction
        return Response({"message": "سوال دنباله‌دار با موفقیت اضافه شد!"}, status.HTTP_200_OK)


def get_random(query_set):
    pks = query_set.values_list('pk', flat=True).order_by('id')
    random_pk = choice(pks)
    return query_set.get(pk=random_pk)


def make_transaction(player, title, value):
    new_transaction = Transaction()
    new_transaction.player = player
    new_transaction.title = title
    new_transaction.amount = new_transaction.amount + value
    new_transaction.save()
