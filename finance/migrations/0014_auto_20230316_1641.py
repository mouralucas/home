# Generated by Django 3.2.15 on 2023-03-16 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0013_auto_20230315_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankstatement',
            name='cash_flow',
            field=models.CharField(choices=[('OUTGOING', 'Saída'), ('INCOMING', 'Entrada'), ('MONTHLY_BALANCE', 'Saldo mensal')], max_length=100),
        ),
        migrations.AlterField(
            model_name='creditcardbill',
            name='cash_flow',
            field=models.CharField(choices=[('OUTGOING', 'Saída'), ('INCOMING', 'Entrada'), ('MONTHLY_BALANCE', 'Saldo mensal')], max_length=100),
        ),
    ]
