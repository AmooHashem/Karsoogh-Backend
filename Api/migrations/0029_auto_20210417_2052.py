# Generated by Django 3.0.4 on 2021-04-17 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0028_exam_prerequisite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='ending_date',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='holding_date',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='min_score',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='status',
        ),
        migrations.AddField(
            model_name='exam',
            name='finish_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='تاریخ پایان'),
        ),
        migrations.AddField(
            model_name='exam',
            name='required_score',
            field=models.IntegerField(default=0, verbose_name='کف قبولی'),
        ),
        migrations.AddField(
            model_name='exam',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='تاریخ شروع'),
        ),
    ]
