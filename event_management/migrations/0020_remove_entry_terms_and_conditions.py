# Generated by Django 5.0.3 on 2024-03-31 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event_management', '0019_entry_terms_and_conditions_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='terms_and_conditions',
        ),
    ]
