# Generated by Django 3.2.15 on 2023-04-05 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_auto_20230404_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankstatement',
            name='bank_fee',
            field=models.DecimalField(decimal_places=5, default=0, help_text='Spread do banco, aplicado sobre a cotação', max_digits=14),
        ),
        migrations.AlterField(
            model_name='bankstatement',
            name='tax',
            field=models.DecimalField(decimal_places=5, default=0, help_text='Iof, aplicado sobre a cotação', max_digits=14),
        ),
    ]