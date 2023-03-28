# Generated by Django 3.2.15 on 2023-03-28 14:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0009_reading_is_dropped'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='owner',
            field=models.ForeignKey(default='adf52a1e-7a19-11ed-a1eb-0242ac120002', on_delete=django.db.models.deletion.DO_NOTHING, to='user.account'),
            preserve_default=False,
        ),
    ]
