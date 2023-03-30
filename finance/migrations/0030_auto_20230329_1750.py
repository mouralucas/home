# Generated by Django 3.2.15 on 2023-03-29 20:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0029_alter_bankstatement_account_old'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='dat_maturity',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='investment',
            name='amount',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='investment',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='investment',
            name='name',
            field=models.CharField(default='ajustar', max_length=200),
            preserve_default=False,
        ),
    ]
