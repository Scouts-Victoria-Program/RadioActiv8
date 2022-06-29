# Generated by Django 4.0.5 on 2022-06-29 23:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scoutsvic_extranet', '0004_historicalmemberclass_priority_memberclass_priority'),
        ('RadioActiv8', '0023_patrol_preferred_bases'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpatrol',
            name='member_class',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='scoutsvic_extranet.memberclass'),
        ),
        migrations.AddField(
            model_name='historicalpatrol',
            name='project_patrol',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='patrol',
            name='member_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scoutsvic_extranet.memberclass'),
        ),
        migrations.AddField(
            model_name='patrol',
            name='project_patrol',
            field=models.BooleanField(default=False),
        ),
    ]