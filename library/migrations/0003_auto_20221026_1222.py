# Generated by Django 3.2.15 on 2022-10-26 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_auto_20220909_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='cover',
            field=models.FileField(default='library/item/cover/no_cover.png', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='item',
            name='publisher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='library_item_publisher', to='library.publisher'),
        ),
    ]