from django.contrib import admin

from Game.models import Game, Player, PlayerProblem, Transaction, Subject, Hint, PlayerMultipleProblem, \
    PlayerSingleProblem, Problem, MultipleProblem

admin.site.register(Game)
admin.site.register(Problem)
admin.site.register(MultipleProblem)
admin.site.register(Player)
admin.site.register(PlayerSingleProblem)
admin.site.register(PlayerMultipleProblem)
admin.site.register(PlayerProblem)
admin.site.register(Transaction)
admin.site.register(Hint)
admin.site.register(Subject)
