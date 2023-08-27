# Generated by Django 4.2.3 on 2023-08-27 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0019_investmentstatement'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountbalance',
            name='previous_balance',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Saldo da conta antes do período', max_digits=14),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='financedata',
            name='periodicity_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='financedata',
            name='type_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
