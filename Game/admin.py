import csv

from django.contrib import admin
from django.contrib.auth.hashers import make_password
from Account.models import User
from Game.models import Game, Player, PlayerProblem, Transaction, Subject, Hint, PlayerMultipleProblem, \
    PlayerSingleProblem, Problem, MultipleProblem

admin.site.register(MultipleProblem)
admin.site.register(PlayerSingleProblem)
admin.site.register(PlayerMultipleProblem)
admin.site.register(Transaction)
admin.site.register(Hint)
admin.site.register(Game)
admin.site.register(Subject)


# with open(path) as f:
#     reader = csv.reader(f)
#     for row in reader:
#         _, created = Teacher.objects.get_or_create(
#             first_name=row[0],
#             last_name=row[1],
#             middle_name=row[2],
#         )
#         # creates a tuple of the new object or
#         # current object and a boolean of if it was created


def import_from_csv(a, b, c):
    with open('students_info.csv') as f:
        reader = csv.reader(f)
        boys_game = Game.objects.get(title='پسرانه')
        girls_game = Game.objects.get(title='دخترانه')
        for row in reader:
            if row[5] == 'MAN':
                game = boys_game
            else:
                game = girls_game
            user, _ = User.objects.get_or_create(
                password=make_password(row[2]),
                username=row[2],
                first_name=row[3],
                last_name=row[4],
                phone_number=row[7],
                backup_phone_number=row[8]
            )
            Player.objects.get_or_create(
                user=user,
                game=game)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    import_from_csv.short_description = 'بارگذاری دانش‌آموزان در سایت'
    actions = [import_from_csv]
    list_display = ('user', 'game', 'score', 'id')


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'difficulty', 'cost', 'reward', 'id')
