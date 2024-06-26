# Generated by Django 5.0.3 on 2024-04-05 17:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_management', '0025_alter_race_entry_fee'),
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='payment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entry', to='payments.payment'),
        ),
    ]
