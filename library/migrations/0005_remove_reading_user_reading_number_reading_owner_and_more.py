# Generated by Django 4.2.3 on 2023-11-09 22:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0004_alter_reading_start_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reading',
            name='user',
        ),
        migrations.AddField(
            model_name='reading',
            name='number',
            field=models.SmallIntegerField(default=1, help_text="Indicate if it's the fist, second... time the user reads the item"),
        ),
        migrations.AddField(
            model_name='reading',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='readingprogress',
            name='rate',
            field=models.SmallIntegerField(null=True),
        ),
    ]
