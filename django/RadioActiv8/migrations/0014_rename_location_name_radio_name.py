# Generated by Django 4.0 on 2021-12-23 07:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("RadioActiv8", "0013_gpstracker_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="radio",
            old_name="location_name",
            new_name="name",
        ),
    ]
