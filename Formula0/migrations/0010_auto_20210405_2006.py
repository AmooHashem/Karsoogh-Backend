# Generated by Django 3.0.4 on 2021-04-05 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Formula0', '0009_auto_20210405_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemteam',
            name='answer',
            field=models.TextField(blank=True, null=True, verbose_name='پاسخ'),
        ),
    ]
