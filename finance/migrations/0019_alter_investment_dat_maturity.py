# Generated by Django 3.2.15 on 2023-04-13 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0018_investment_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='dat_maturity',
            field=models.DateField(null=True),
        ),
    ]