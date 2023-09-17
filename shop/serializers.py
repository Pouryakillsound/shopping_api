import decimal
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from rest_framework import serializers

from .models import Cart, CartItem, Collection, Order, Product, ProductImage


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
    collection_id = serializers.IntegerField()
    class Meta:
        model = Product
        fields = ['title', 'description', 'inventory',
                  'unit_price', 'collection_id']
        images = serializers.ImageField()


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ['id', 'title', 'featured_product']


class CartItemSerializer(serializers.ModelSerializer):
    total_price_product = serializers.SerializerMethodField(method_name='total_item_price')
    product = ProductSerializer()
    cart_id = serializers.CharField(read_only=True)
    class Meta:
        model = CartItem
        fields = ['id', 'cart_id', 'product', 'quantity', 'total_price_product']

    def total_item_price(self, cart_item):
        return cart_item.quantity * cart_item.product.unit_price



class CreateCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, product_id):
        if not Product.objects.filter(pk=product_id):
            raise ValidationError('Product id is not correct')
        return product_id

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        quantity = self.validated_data['quantity']
        product_id = self.validated_data['product_id']

        try:
            cartitem = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cartitem.quantity += quantity
            cartitem.save()
            self.instance = cartitem
            return self.instance

        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(product_id=product_id,
                                                cart_id=cart_id,
                                                  quantity=quantity)
            return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

class UpdteCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta:
        model = CartItem
        fields = ['product_id', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    cart_price = serializers.SerializerMethodField(method_name='total_cart_price')

    class Meta:
        model = Cart
        fields = ['id', 'items', 'created_at', 'cart_price']

    def total_cart_price(self, cart):
        price = 0
        for item in cart.items.all():
            price += item.quantity * item.product.unit_price
        return price
