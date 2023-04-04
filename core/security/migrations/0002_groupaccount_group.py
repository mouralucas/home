# Generated by Django 3.2.15 on 2023-04-02 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupaccount',
            name='group',
            field=models.ForeignKey(default='user', on_delete=django.db.models.deletion.DO_NOTHING, to='security.group'),
            preserve_default=False,
        ),
    ]