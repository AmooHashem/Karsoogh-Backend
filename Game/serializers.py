from rest_framework import serializers
from .models import *


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'title']


class ProblemDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        exclude = ['answer', 'games']


class MultipleProblemDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleProblem
        fields = '__all__'


class ProblemInfoSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()

    class Meta:
        model = Problem
        fields = ['id', 'title', 'subject', 'difficulty', ]


class MultipleProblemInfoSerializer(serializers.ModelSerializer):
    problems_count = serializers.SerializerMethodField()

    class Meta:
        model = MultipleProblem
        fields = ['id', 'title', 'problems_count']

    def get_problems_count(self, obj):
        return obj.problems.count()


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
