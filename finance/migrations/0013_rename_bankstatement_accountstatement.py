# Generated by Django 4.2.3 on 2023-08-13 14:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0007_delete_tipo'),
        ('finance', '0012_remove_bankstatement_account_old'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BankStatement',
            new_name='AccountStatement',
        ),
    ]
