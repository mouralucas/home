# Generated by Django 4.2.3 on 2023-11-09 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_rename_dat_created_author_created_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reading',
            old_name='dat_end',
            new_name='end_at',
        ),
        migrations.RenameField(
            model_name='reading',
            old_name='dat_start',
            new_name='start_at',
        ),
        migrations.AlterField(
            model_name='readingprogress',
            name='date',
            field=models.DateField(),
        ),
    ]
