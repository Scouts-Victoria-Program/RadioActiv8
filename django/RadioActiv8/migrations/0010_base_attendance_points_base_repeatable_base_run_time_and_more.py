# Generated by Django 4.0 on 2021-12-22 06:48

import datetime

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("RadioActiv8", "0009_participant"),
    ]

    operations = [
        migrations.AddField(
            model_name="base",
            name="attendance_points",
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name="base",
            name="repeatable",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="base",
            name="run_time",
            field=models.DurationField(default=datetime.timedelta(seconds=300)),
        ),
        migrations.AddField(
            model_name="intelligence",
            name="completion_points",
            field=models.IntegerField(default=200),
        ),
        migrations.AddField(
            model_name="radio",
            name="description",
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name="intelligence",
            name="base",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="RadioActiv8.base",
            ),
        ),
    ]
