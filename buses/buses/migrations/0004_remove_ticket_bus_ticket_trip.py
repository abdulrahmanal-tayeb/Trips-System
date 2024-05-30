# Generated by Django 5.0.1 on 2024-05-30 09:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buses', '0003_rename_available_seats_trip_passengers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='bus',
        ),
        migrations.AddField(
            model_name='ticket',
            name='trip',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='buses.trip'),
            preserve_default=False,
        ),
    ]
