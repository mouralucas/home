# Generated by Django 3.2.15 on 2023-03-31 00:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0033_auto_20230330_2122'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='owner_old',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='bankstatement',
            old_name='owner_old',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='creditcard',
            old_name='owner_old',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='creditcardbill',
            old_name='owner_old',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='investment',
            old_name='owner_old',
            new_name='owner',
        ),
    ]
