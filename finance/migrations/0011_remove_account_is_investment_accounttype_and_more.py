# Generated by Django 4.2.3 on 2023-11-22 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0010_account_is_investment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='is_investment',
        ),
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('edited_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=500)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_last_edit_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'finance"."account_type',
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='finance.accounttype'),
        ),
    ]