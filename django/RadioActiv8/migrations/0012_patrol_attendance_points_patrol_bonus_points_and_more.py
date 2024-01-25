# Generated by Django 4.0 on 2021-12-23 00:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("RadioActiv8", "0011_patrol_current_base"),
    ]

    operations = [
        migrations.AddField(
            model_name="patrol",
            name="attendance_points",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="patrol",
            name="bonus_points",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="patrol",
            name="completion_points",
            field=models.IntegerField(default=0),
        ),
    ]
