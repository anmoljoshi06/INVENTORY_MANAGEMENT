# Generated by Django 3.2.3 on 2021-09-17 18:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0014_bakery_item_names_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bakery_item_names',
            name='discount',
            field=models.IntegerField(blank=True, default=0, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
    ]