# Generated by Django 3.2.15 on 2023-04-02 21:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_rename_father_category_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Access',
            fields=[
                ('status', models.BooleanField(default=True, null=True)),
                ('dat_created', models.DateTimeField(blank=True, null=True)),
                ('dat_last_edited', models.DateTimeField(blank=True, null=True)),
                ('dat_deleted', models.DateTimeField(blank=True, null=True)),
                ('id', models.CharField(max_length=150, primary_key=True, serialize=False)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='security_access_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='security_access_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='security_access_last_edit_by', to=settings.AUTH_USER_MODEL)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.module')),
            ],
            options={
                'db_table': 'security"."access',
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('status', models.BooleanField(default=True, null=True)),
                ('dat_created', models.DateTimeField(blank=True, null=True)),
                ('dat_last_edited', models.DateTimeField(blank=True, null=True)),
                ('dat_deleted', models.DateTimeField(blank=True, null=True)),
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=500, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='security_profile_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='security_profile_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='security_profile_last_edit_by', to=settings.AUTH_USER_MODEL)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.module')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='security.profile')),
            ],
            options={
                'db_table': 'security"."profile',
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ProfileAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, null=True)),
                ('dat_created', models.DateTimeField(blank=True, null=True)),
                ('dat_last_edited', models.DateTimeField(blank=True, null=True)),
                ('dat_deleted', models.DateTimeField(blank=True, null=True)),
                ('dat_start', models.DateField(null=True)),
                ('dat_end', models.DateField(null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='security_profileaccount_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='security_profileaccount_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='security_profileaccount_last_edit_by', to=settings.AUTH_USER_MODEL)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='security.profile')),
            ],
            options={
                'db_table': 'security"."profile_account',
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ProfileAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, null=True)),
                ('dat_created', models.DateTimeField(blank=True, null=True)),
                ('dat_last_edited', models.DateTimeField(blank=True, null=True)),
                ('dat_deleted', models.DateTimeField(blank=True, null=True)),
                ('access', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='security.access')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='security_profileaccess_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='security_profileaccess_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='security_profileaccess_last_edit_by', to=settings.AUTH_USER_MODEL)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='security.profile')),
            ],
            options={
                'db_table': 'security"."profile_access',
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='GroupAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, null=True)),
                ('dat_created', models.DateTimeField(blank=True, null=True)),
                ('dat_last_edited', models.DateTimeField(blank=True, null=True)),
                ('dat_deleted', models.DateTimeField(blank=True, null=True)),
                ('code', models.CharField(max_length=50, null=True)),
                ('dat_start', models.DateField(null=True)),
                ('dat_end', models.DateField(null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='security_groupaccount_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='security_groupaccount_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='security_groupaccount_last_edit_by', to=settings.AUTH_USER_MODEL)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='security.profile')),
            ],
            options={
                'db_table': 'security"."group_account',
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('status', models.BooleanField(default=True, null=True)),
                ('dat_created', models.DateTimeField(blank=True, null=True)),
                ('dat_last_edited', models.DateTimeField(blank=True, null=True)),
                ('dat_deleted', models.DateTimeField(blank=True, null=True)),
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=500, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='security_group_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='security_group_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='security_group_last_edit_by', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='security.group')),
            ],
            options={
                'db_table': 'security"."group',
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
