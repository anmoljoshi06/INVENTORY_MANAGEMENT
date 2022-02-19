from .models import *
from rest_framework import serializers


class ingredients_serializer(serializers.ModelSerializer):
    class Meta:
        model = ingredients
        fields = '__all__'

class Bakery_Item_Names_serializer(serializers.ModelSerializer):
    class Meta:
        model = Bakery_Item_Names
        fields = '__all__'

class Bakery_item_recipe_serializer(serializers.ModelSerializer):
    class Meta:
        model = Bakery_item_recipe
        fields = '__all__'


class user_menu_serializer(serializers.ModelSerializer):
    class Meta:
        model = Bakery_Item_Names
        fields = ("bakery_item","price",)


class orders_serializer(serializers.ModelSerializer):
    class Meta:
        model = orders
        fields = ("bakery_item" ,"order_date","order_time","quantity","cost", )


class Single_ingredients_serializer(serializers.ModelSerializer):
    class Meta:
        model = ingredients
        fields = ("item",)

class Bakery_item_detail_serializer(serializers.ModelSerializer):
    item =  serializers.SlugRelatedField(read_only=True,slug_field='item')
    class Meta:
        model = Bakery_item_recipe
        fields = ("percentage","item",)



