from django.db import models


class Game(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان')
    start_date = models.DateTimeField(verbose_name='تاریخ شروع', null=True, blank=True)
    finish_date = models.DateTimeField(verbose_name='تاریخ پایان', null=True, blank=True)

    def __str__(self):
        return self.title
