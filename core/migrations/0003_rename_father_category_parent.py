# Generated by Django 3.2.15 on 2023-02-22 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20221212_1114'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='father',
            new_name='parent',
        ),
    ]