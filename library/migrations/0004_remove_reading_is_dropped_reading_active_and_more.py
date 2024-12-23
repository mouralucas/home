# Generated by Django 4.2.10 on 2024-04-03 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('library', '0003_rename_finish_dt_reading_finish_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reading',
            name='is_dropped',
        ),
        migrations.AddField(
            model_name='reading',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='reading',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.status'),
        ),
    ]
