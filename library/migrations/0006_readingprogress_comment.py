# Generated by Django 4.2.3 on 2023-11-10 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_remove_reading_user_reading_number_reading_owner_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='readingprogress',
            name='comment',
            field=models.CharField(max_length=500, null=True),
        ),
    ]