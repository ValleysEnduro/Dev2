# Generated by Django 5.0.3 on 2024-03-31 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_management', '0016_remove_event_depth_remove_event_numchild_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='race',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
