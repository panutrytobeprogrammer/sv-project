# Generated by Django 4.1.6 on 2023-03-21 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_delete_planning_temp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Planning_temp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plantype', models.CharField(max_length=255)),
                ('og', models.CharField(max_length=255)),
                ('start', models.DateTimeField()),
                ('ds', models.CharField(max_length=255)),
                ('arrv', models.DateTimeField()),
                ('traveltime', models.PositiveIntegerField()),
                ('extratime', models.IntegerField()),
            ],
        ),
    ]