# Generated by Django 3.2.15 on 2023-03-10 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0003_apiintegration'),
    ]

    operations = [
        migrations.AddField(
            model_name='apiintegration',
            name='params',
            field=models.TextField(null=True),
        ),
    ]