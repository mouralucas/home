# Generated by Django 4.2.3 on 2023-08-12 01:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0010_alter_creditcardbill_amount_reference_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='creditcardbill',
            old_name='price_currency_dollar',
            new_name='dollar_currency_quote',
        ),
    ]
