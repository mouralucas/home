# Generated by Django 3.2.15 on 2022-12-12 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='dat_created',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bankstatement',
            name='dat_created',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='categorygroup',
            name='dat_created',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='categorytype',
            name='dat_created',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='dat_created',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='creditcardbill',
            name='dat_created',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='currency',
            name='dat_created',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='currencyrate',
            name='dat_created',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investimenttype',
            name='dat_created',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='dat_created',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investmentstatement',
            name='dat_created',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]