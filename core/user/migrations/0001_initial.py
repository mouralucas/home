# Generated by Django 3.2 on 2022-08-08 00:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=200, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_first_login', models.BooleanField(default=True)),
                ('hash', models.UUIDField(default=uuid.uuid4, null=True)),
            ],
            options={
                'db_table': 'public"."account',
            },
        ),
    ]
