# Generated by Django 4.2.10 on 2024-04-03 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_rename_end_at_reading_finish_dt_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reading',
            old_name='finish_dt',
            new_name='finish_date',
        ),
        migrations.RenameField(
            model_name='reading',
            old_name='start_dt',
            new_name='start_date',
        ),
    ]
