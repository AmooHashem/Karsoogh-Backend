from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from Game.models import Problem
from .serializers import AuctionSerializers

# Create your views here.

class CreateAuctionProblem(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AuctionSerializers
    queryset = Auction.objects.all()


    def perform_create(self, serializer):
        auction_obj = serializer.save()
        player_user = Player.objects.get(user=self.request.user)
        problem = Problem.objects.get(id=self.request.data.get('problem_id'))
        auction_obj.player = player_user
        auction_obj.problem_for_sell = problem
        # auction_obj.problem_for_sell = self.request.query_params.get('problem_id')
        auction_obj.save()