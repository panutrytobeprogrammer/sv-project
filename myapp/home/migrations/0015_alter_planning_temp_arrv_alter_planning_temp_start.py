# Generated by Django 4.1.6 on 2023-03-19 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_planning_temp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planning_temp',
            name='arrv',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='planning_temp',
            name='start',
            field=models.DateTimeField(),
        ),
    ]
