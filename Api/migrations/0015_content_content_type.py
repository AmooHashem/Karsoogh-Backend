# Generated by Django 3.1.6 on 2021-02-24 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0014_auto_20210225_0031'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='content_type',
            field=models.IntegerField(choices=[(1, 'متن'), (2, 'ویدئو'), (3, 'عکس'), (4, 'بازی')], default=1, verbose_name='نوع محتوا'),
        ),
    ]
