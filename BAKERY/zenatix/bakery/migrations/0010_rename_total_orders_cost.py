# Generated by Django 3.2.3 on 2021-09-16 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0009_alter_orders_bakery_item'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='total',
            new_name='cost',
        ),
    ]
