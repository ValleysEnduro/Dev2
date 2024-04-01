# Generated by Django 5.0.3 on 2024-04-01 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_management', '0022_entry_entry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='entry_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='race',
            name='entry_close_datetime',
            field=models.DateTimeField(help_text='Deadline after which no new entries are accepted.'),
        ),
        migrations.AlterField(
            model_name='race',
            name='transfer_close_datetime',
            field=models.DateTimeField(help_text='Deadline after which entries cannot be transferred.'),
        ),
    ]
