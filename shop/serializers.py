from rest_framework import serializers
from .models import Product, Collection, Order
from django.utils.text import slugify
from django.core.exceptions import ValidationError

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    images = serializers.ImageField(required=False)


    def update(self, instance, validated_data):
        instance.slug = slugify(validated_data.get('title', instance.title))
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.inventory = validated_data.get('inventory', instance.inventory)
        instance.unit_price = validated_data.get('unit_price', instance.unit_price)
        instance.collection = validated_data.get('collection', instance.collection)
        instance.promotion_set = validated_data.get('promotion', instance.promotion)
        instance.images_set = validated_data.get('images', instance.images)
        instance.save()
        return instance


    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'inventory',
                  'unit_price', 'collection', 'promotion', 'images']

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'featured_product']

class OrderSerializer(serializers.ModelSerializer):
    placed_at = serializers.DateTimeField(read_only=True)



    class Meta:
        model = Order
        fields = ['user', 'payment_status', 'placed_at']
