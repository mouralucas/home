# Generated by Django 3.2.14 on 2022-08-14 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_category_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.DecimalField(decimal_places=4, max_digits=10, null=True),
        ),
    ]