# Generated by Django 3.1.6 on 2021-02-13 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0009_auto_20210213_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='school_name',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='نام مدرسه'),
        ),
        migrations.AlterField(
            model_name='school',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='کد مدرسه'),
        ),
        migrations.AlterField(
            model_name='school',
            name='title',
            field=models.CharField(max_length=255, verbose_name='عنوان مدرسه'),
        ),
    ]
