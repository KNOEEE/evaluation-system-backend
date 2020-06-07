# Generated by Django 3.0.3 on 2020-04-23 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Model', '0002_auto_20200418_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rate',
            field=models.FloatField(verbose_name='评分'),
        ),
        migrations.AlterField(
            model_name='course',
            name='cid',
            field=models.CharField(max_length=5, unique=True, verbose_name='课程号'),
        ),
        migrations.AlterField(
            model_name='student',
            name='sid',
            field=models.CharField(max_length=10, unique=True, verbose_name='学号'),
        ),
    ]
