# Generated by Django 3.2.10 on 2021-12-13 00:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("RadioActiv8", "0002_delete_queue"),
    ]

    operations = [
        migrations.CreateModel(
            name="Session",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128)),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name="event",
            name="session",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="RadioActiv8.session",
            ),
        ),
        migrations.AddField(
            model_name="location",
            name="session",
            field=models.ManyToManyField(to="RadioActiv8.Session"),
        ),
        migrations.AddField(
            model_name="patrol",
            name="session",
            field=models.ManyToManyField(to="RadioActiv8.Session"),
        ),
    ]
