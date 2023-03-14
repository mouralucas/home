# Generated by Django 3.2.15 on 2023-03-14 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0011_auto_20230313_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankstatement',
            name='amount_absolute',
            field=models.DecimalField(decimal_places=2, default=0, help_text='O mesmo do amount sem o sinal', max_digits=14),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='creditcardbill',
            name='amount_absolute',
            field=models.DecimalField(decimal_places=2, default=0, help_text='O mesmo do amount sem o sinal', max_digits=14),
            preserve_default=False,
        ),
    ]
