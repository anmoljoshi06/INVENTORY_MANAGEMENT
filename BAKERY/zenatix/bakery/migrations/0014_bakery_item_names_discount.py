# Generated by Django 3.2.3 on 2021-09-17 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0013_remove_bakery_item_names_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='bakery_item_names',
            name='discount',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]