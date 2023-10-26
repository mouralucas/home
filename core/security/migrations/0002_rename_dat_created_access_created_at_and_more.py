# Generated by Django 4.2.3 on 2023-10-11 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='access',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='access',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='access',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='groupaccount',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='groupaccount',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='groupaccount',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='profileaccess',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='profileaccess',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='profileaccess',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='profileaccount',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='profileaccount',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='profileaccount',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
    ]