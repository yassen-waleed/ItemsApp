# Generated by Django 4.0.3 on 2022-06-22 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Items', '0002_item_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='size',
            field=models.IntegerField(default=100, max_length=10),
        ),
    ]
