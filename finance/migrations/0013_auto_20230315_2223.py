# Generated by Django 3.2.15 on 2023-03-16 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0012_auto_20230313_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankstatement',
            name='period',
            field=models.IntegerField(help_text='Período de referência', null=True),
        ),
        migrations.AlterField(
            model_name='categorygroup',
            name='group',
            field=models.CharField(choices=[('fixed_expenses', 'Despesas fixas'), ('variable_expenses', 'Despesas variáveis'), ('not_expense', 'Não é despesa')], default='variable_expenses', max_length=50),
        ),
        migrations.AlterField(
            model_name='creditcardbill',
            name='period',
            field=models.IntegerField(help_text='Período de referência', null=True),
        ),
    ]