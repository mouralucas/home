# Generated by Django 4.2.7 on 2024-01-29 14:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0030_investmentgoal_owner_alter_investmentgoal_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcardbill',
            name='credit_card',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='investmentgoal',
            name='id',
            field=models.UUIDField(default=uuid.UUID('d4e9a6f2-0a12-413a-91c6-7aec9b58f5cb'), primary_key=True, serialize=False),
        ),
    ]
