# Generated by Django 5.0.3 on 2024-03-30 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event_management', '0010_auto_20240330_1602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='depth',
        ),
        migrations.RemoveField(
            model_name='event',
            name='level',
        ),
        migrations.RemoveField(
            model_name='event',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='event',
            name='numchild',
        ),
        migrations.RemoveField(
            model_name='event',
            name='path',
        ),
        migrations.RemoveField(
            model_name='event',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='event',
            name='tree_id',
        ),
        migrations.RemoveField(
            model_name='race',
            name='depth',
        ),
        migrations.RemoveField(
            model_name='race',
            name='numchild',
        ),
        migrations.RemoveField(
            model_name='race',
            name='path',
        ),
    ]
