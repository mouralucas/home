# Generated by Django 4.2.3 on 2023-08-05 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_brazilinterestrate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brazilinterestrate',
            name='cdi',
            field=models.DecimalField(decimal_places=6, max_digits=20),
        ),
        migrations.AlterField(
            model_name='brazilinterestrate',
            name='selic',
            field=models.DecimalField(decimal_places=6, max_digits=20),
        ),
    ]
