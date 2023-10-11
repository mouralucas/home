# Generated by Django 4.2.3 on 2023-10-11 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='author',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='author',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='collection',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='collection',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='collection',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='itemauthor',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='itemauthor',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='itemauthor',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='itemstatus',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='itemstatus',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='itemstatus',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='publisher',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='publisher',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='publisher',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='reading',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='reading',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='reading',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='readingprogress',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='readingprogress',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='readingprogress',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='serie',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='serie',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='serie',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
    ]
