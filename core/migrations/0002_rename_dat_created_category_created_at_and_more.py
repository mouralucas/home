# Generated by Django 4.2.3 on 2023-10-11 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='city',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='city',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='city',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='country',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='country',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='country',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='dynamictexttranslation',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='dynamictexttranslation',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='dynamictexttranslation',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='language',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='language',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='language',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='module',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='module',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='module',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='periodicity',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='periodicity',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='periodicity',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='region',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='region',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='region',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='state',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='state',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='state',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='status',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='status',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='status',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='systemlanguages',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='systemlanguages',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='systemlanguages',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='type',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='type',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='type',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='uf',
            old_name='dat_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='uf',
            old_name='dat_deleted',
            new_name='deleted_at',
        ),
        migrations.RenameField(
            model_name='uf',
            old_name='dat_last_edited',
            new_name='edited_at',
        ),
    ]
