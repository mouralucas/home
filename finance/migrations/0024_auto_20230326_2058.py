# Generated by Django 3.2.15 on 2023-03-26 23:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0023_investment_custodian'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditcard',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='finance.account'),
        ),
        migrations.AddField(
            model_name='investment',
            name='owner',
            field=models.ForeignKey(default='adf52a1e-7a19-11ed-a1eb-0242ac120002', on_delete=django.db.models.deletion.DO_NOTHING, to='user.account'),
            preserve_default=False,
        ),
    ]
