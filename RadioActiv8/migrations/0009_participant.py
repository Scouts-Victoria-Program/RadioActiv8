# Generated by Django 4.0 on 2021-12-20 05:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RadioActiv8', '0008_alter_event_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_id', models.IntegerField(null=True)),
                ('full_name', models.CharField(max_length=128)),
                ('preferred_name', models.CharField(max_length=128)),
                ('type', models.CharField(blank=True, choices=[('J', 'Joey'), ('C', 'Cub'), ('S', 'Scout'), ('V', 'Venturer'), ('R', 'Rover'), ('L', 'Leader')], default='S', max_length=1)),
                ('patrol', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='RadioActiv8.patrol')),
            ],
        ),
    ]