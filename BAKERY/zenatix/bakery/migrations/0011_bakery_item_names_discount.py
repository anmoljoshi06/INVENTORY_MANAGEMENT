# Generated by Django 3.2.3 on 2021-09-17 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0010_rename_total_orders_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='bakery_item_names',
            name='discount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]