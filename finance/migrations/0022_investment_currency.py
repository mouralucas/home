# Generated by Django 4.2.7 on 2024-01-05 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0021_taxfeetype'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='currency',
            field=models.ForeignKey(default='BRL', on_delete=django.db.models.deletion.DO_NOTHING, to='finance.currency'),
            preserve_default=False,
        ),
    ]
