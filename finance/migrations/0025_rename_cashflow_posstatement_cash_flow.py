# Generated by Django 4.2.7 on 2024-01-11 01:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0024_posstatement'),
    ]

    operations = [
        migrations.RenameField(
            model_name='posstatement',
            old_name='cashFlow',
            new_name='cash_flow',
        ),
    ]
