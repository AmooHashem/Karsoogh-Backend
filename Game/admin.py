from django.contrib import admin

from Game.models import Game, Player, Problem, ConsecutiveProblems, PlayerProblem, Transaction, Subject, Hint

admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Problem)
admin.site.register(ConsecutiveProblems)
admin.site.register(PlayerProblem)
admin.site.register(Transaction)
admin.site.register(Hint)
admin.site.register(Subject)
