from django.contrib import admin

from Game.models import Game, Player, Problem, ConsecutiveProblems, Answer, Transaction

admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Problem)
admin.site.register(ConsecutiveProblems)
admin.site.register(Answer)
admin.site.register(Transaction)
