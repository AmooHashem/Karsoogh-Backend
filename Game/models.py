from django.db import models
from django.utils.safestring import mark_safe
from jsonfield import JSONField

from Account.models import User


class Game(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان')
    start_date = models.DateTimeField(verbose_name='تاریخ شروع')
    finish_date = models.DateTimeField(verbose_name='تاریخ پایان')

    def __str__(self):
        return self.title


class Player(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, verbose_name='کاربر')
    game = models.ForeignKey(to=Game, on_delete=models.PROTECT, verbose_name='بازی')
    score = models.IntegerField(default=0, verbose_name='امتیاز')

    def __str__(self):
        return f'{self.user} | {self.game.title}'


class Subject(models.Model):
    title = models.CharField(max_length=30, verbose_name='عنوان')

    def __str__(self):
        return f'{self.title}'


class Problem(models.Model):
    class Difficulty(models.TextChoices):
        EASY = 'EASY'
        MEDIUM = 'MEDIUM'
        HARD = 'HARD'

    title = models.CharField(max_length=100, verbose_name='عنوان')
    games = models.ManyToManyField(Game, verbose_name='بازی‌(ها)')
    subject = models.ForeignKey(to=Subject, on_delete=models.PROTECT, blank=True, null=True)
    difficulty = models.CharField(max_length=20, choices=Difficulty.choices, verbose_name='درجه سختی',
                                  default=Difficulty.MEDIUM)
    text = models.TextField(verbose_name='متن')
    short_answer = models.CharField(max_length=100, null=True, blank=True, verbose_name='پاسخ کوتاه (اختیاری)')

    def __str__(self):
        return f'{self.title}'


class PlayerProblem(models.Model):
    class Status(models.Choices):
        RECEIVED = 'RECEIVED'
        DELIVERED = 'DELIVERED'
        SCORED = 'SCORED'

    problem = models.ForeignKey(Problem, on_delete=models.PROTECT, verbose_name='مسئله')
    player = models.ForeignKey(Player, on_delete=models.PROTECT, verbose_name='بازیکن')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.RECEIVED)
    mark = models.IntegerField(default=-1, verbose_name='نمره')
    text_answer = models.TextField(verbose_name='متن پاسخ')
    file_answer = models.FileField(upload_to='game-answers/', blank=True, null=True)


class ConsecutiveProblems(models.Model):
    problems = models.ManyToManyField(Problem, verbose_name='مسئله‌ها')
    hint_count = models.IntegerField(default=0)


class Transaction(models.Model):
    player = models.ForeignKey(to=Player, on_delete=models.PROTECT, verbose_name='بازیکن')
    title = models.CharField(max_length=100, verbose_name='عنوان')
    amount = models.IntegerField(verbose_name='مقدار')

    def __str__(self):
        return f'{self.title} | {self.player}'


class Hint(models.Model):
    consecutive_problems = models.ForeignKey(ConsecutiveProblems, on_delete=models.PROTECT, verbose_name='سری مسئله')
    text = models.TextField(default='درخواست راهنمایی شما ثبت شد! به زودی منتظر راهنمایی خ')
