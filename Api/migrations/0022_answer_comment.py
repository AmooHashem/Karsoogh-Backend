# Generated by Django 3.0.4 on 2021-03-29 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0021_auto_20210328_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='نظر مصحح'),
        ),
    ]
