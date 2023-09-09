from django.core.exceptions import ValidationError
from django.utils.text import slugify
from rest_framework import serializers

from .models import Cart, Collection, Order, Product, ProductImage


class ProductImageNestedToProductListSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        image = validated_data['image']
        product_pk = self.context['product_pk']
        product_image = ProductImage.objects.create(image=image, product_id=product_pk)
        return product_image

    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductImageNestedToProductDetailSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.image = validated_data['image']
        instance.save()
        return instance
        
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):

    images = ProductImageNestedToProductListSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'inventory',
                  'unit_price', 'collection', 'promotion', 'images', 'seller']


class ProductUpdateSerializer(serializers.ModelSerializer):

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
        fields = ['title', 'description', 'inventory',
                  'unit_price', 'collection', 'promotion', 'images']

class ProductAddSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        slug = slugify(validated_data['title'])
        request = self.context['request']
        seller = request.user
        product = Product.objects.create(slug=slug, seller=seller, **validated_data)

        return product

    class Meta:
        model = Product
        fields = ['title', 'description', 'inventory',
                  'unit_price', 'collection']
        images = serializers.ImageField()


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ['id', 'title', 'featured_product']


class OrderSerializer(serializers.ModelSerializer):
    placed_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        fields = ['user', 'payment_status', 'placed_at']

class CartSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    items = serializers.RelatedField(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'items', 'created_at']