# Generated by Django 3.2.15 on 2023-03-09 23:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0007_auto_20230307_1219'),
    ]

    operations = [
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('status', models.BooleanField(default=True, null=True)),
                ('dat_created', models.DateTimeField(blank=True, null=True)),
                ('dat_last_edited', models.DateTimeField(blank=True, null=True)),
                ('dat_deleted', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, null=True)),
                ('description', models.TextField(null=True)),
                ('date', models.DateField(null=True)),
                ('quantity', models.DecimalField(decimal_places=5, max_digits=15, null=True)),
                ('price', models.DecimalField(decimal_places=5, help_text='Preço do título no momento da compra', max_digits=15, null=True)),
                ('amount', models.DecimalField(decimal_places=5, max_digits=15, null=True)),
                ('interest_rate', models.CharField(choices=[('FIXED', 'Pré-fixado'), ('FLOATING', 'Pós-fixado'), ('HYBRID', 'Hibrido')], max_length=100)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='finance_investment_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='finance_investment_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='finance_investment_last_edit_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'finance"."investment',
            },
            managers=[
                ('normal_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
