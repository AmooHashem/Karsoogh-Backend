from django.db import models
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


class Problem(models.Model):
    class Level(models.TextChoices):
        EASY = 'EASY'
        MEDIUM = 'MEDIUM'
        HARD = 'HARD'

    games = models.ManyToManyField(Game, verbose_name='بازی‌(ها)')
    title = models.CharField(max_length=100, verbose_name='عنوان')
    text = models.TextField(verbose_name='متن')
    short_answer = models.CharField(max_length=100, null=True, blank=True, verbose_name='پاسخ کوتاه (اختیاری)')
    level = models.CharField(max_length=10, choices=Level.choices, verbose_name='سطح')


class ConsecutiveProblems(models.Model):
    problems = models.ManyToManyField(Problem, verbose_name='مسئله‌ها')
    hint_count = models.IntegerField(default=0)


class Answer(models.Model):
    mark = models.IntegerField(default=-1, verbose_name='نمره')
    problem = models.ForeignKey(Problem, on_delete=models.PROTECT, verbose_name='مسئله')


class Transaction(models.Model):
    player = models.ForeignKey(to=Player, on_delete=models.PROTECT, verbose_name='بازیکن')
    title = models.CharField(max_length=100, verbose_name='عنوان')
    amount = models.IntegerField(verbose_name='مقدار')

    def __str__(self):
        return f'{self.title} | {self.player}'


class Hint(models.Model):
    consecutive_problems = models.ForeignKey(ConsecutiveProblems, on_delete=models.PROTECT, verbose_name='سری مسئله')
    text = models.TextField(default='درخواست راهنمایی شما ثبت شد! به زودی منتظر راهنمایی خ')
