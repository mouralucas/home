# Generated by Django 3.2.15 on 2022-11-06 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0014_alter_bankaccount_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='investmentstatement',
            name='is_validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='investmentstatement',
            name='origin',
            field=models.CharField(default='SYSTEM', max_length=50),
        ),
    ]
