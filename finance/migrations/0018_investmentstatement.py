# Generated by Django 4.2.7 on 2024-01-04 20:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0017_delete_investmentstatement'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvestmentStatement',
            fields=[
                ('status', models.BooleanField(default=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('edited_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('period', models.IntegerField()),
                ('previous_amount', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('gross_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('tax', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('fee', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('net_amount', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('tax_detail', models.JSONField(null=True)),
                ('fee_detail', models.JSONField(null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='finance.currency')),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('investment', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='finance.investment')),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_last_edit_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'finance"."investment_statement',
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]