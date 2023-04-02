# Generated by Django 3.2.15 on 2023-04-02 21:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_rename_father_category_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='category',
            name='owner',
            field=models.ForeignKey(help_text='Category created by the user', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
