# Generated by Django 5.0.3 on 2024-03-31 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_management', '0017_event_is_completed_race_is_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]