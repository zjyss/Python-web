# Generated by Django 2.0.2 on 2020-03-22 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0004_auto_20200321_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='is_default',
            field=models.BooleanField(default=False, verbose_name='是否必修'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='lesson_score',
            field=models.IntegerField(default=0, verbose_name='课程学分'),
        ),
    ]
