from rest_framework import serializers
from .models import *


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'title']


class ProblemDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'
        exclude = ['short_answer', 'games']


class ProblemInfoSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()

    class Meta:
        model = Problem
        fields = ['id', 'title', 'subject', 'difficulty', ]


class MultipleProblemInfoSerializer(serializers.ModelSerializer):
    difficulty = serializers.SerializerMethodField()
    problems_ids = serializers.SerializerMethodField()

    class Meta:
        model = MultipleProblem
        fields = ['id', 'title', 'difficulty', 'problems_ids']

    def get_difficulty(self, obj):
        return obj.problems.count()

    def get_problems_ids(self, obj):
        result = []
        for problem in obj.problems.all():
            result.append(problem.id)
        return result


class SingleProblemSerializer(serializers.ModelSerializer):
    problem = ProblemInfoSerializer()

    class Meta:
        model = PlayerSingleProblem
        fields = ['id', 'status', 'mark', 'problem']


class MultipleProblemSerializer(serializers.ModelSerializer):
    multipleProblem = MultipleProblemInfoSerializer()

    class Meta:
        model = PlayerMultipleProblem
        fields = ['id', 'status', 'mark', 'multipleProblem']
