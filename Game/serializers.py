from rest_framework import serializers
from .models import *


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'title']


class ProblemInfoSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()

    class Meta:
        model = Problem
        fields = ['id', 'title', 'subject', 'difficulty', ]


class PlayerProblemSerializer(serializers.ModelSerializer):
    problem = ProblemInfoSerializer()

    class Meta:
        model = PlayerProblem
        fields = ['id', 'status', 'mark', 'problem']
