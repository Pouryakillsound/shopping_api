from django.core.exceptions import ValidationError
from django.utils.text import slugify
from rest_framework import serializers
from django.db import transaction
from .models import Cart, CartItem, Collection, Order, OrderItem, Product, ProductImage, Review, Promotion
from django.db.models import F
from drf_writable_nested.serializers import WritableNestedModelSerializer


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['title', 'body']

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
    reviews = ReviewSerializer(many=True)
    images = ProductImageNestedToProductListSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'inventory',
                  'unit_price', 'collection', 'promotion', 'images', 'seller', 'reviews']


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


    def validate(self, attrs):
        product_id = attrs['product_id']
        '''
        this part ensures that product_id is related to an object of product table in DB
        '''
        if not Product.objects.filter(pk=product_id).exists():
            raise ValidationError({'product_id': 'Product ID is not correct'})

        product = Product.objects.prefetch_related('cartitem_set__cart').get(id=product_id)
        cart_id = self.context['cart_id']

        '''
        this part will check if cart exists
        '''
        cart_bool = Cart.objects.filter(id = cart_id).exists()
        if not cart_bool:
            raise ValidationError({'cart_id': 'This CART is not valid... create a cart and try adding data to the new existing cart'})
        else:
            pass

        '''
        this will check if the requested quantity for an item is avilable in inventory
        '''
        try:
            cartitem = product.cartitem_set.get(cart_id=cart_id)
            if cartitem.quantity + attrs['quantity'] > product.inventory:
                raise ValidationError({'quantity': 'quantity is getting more than available'})

        except CartItem.DoesNotExist:
            if attrs['quantity'] > product.inventory:
                raise ValidationError({'quantity': 'quantity is more than available'})
            else:
                pass

        return attrs


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

class OrderItemSerailizer(serializers.ModelSerializer):
    order_id = serializers.IntegerField()
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'order_id', 'product', 'quantity', 'unit_price']

class OrderSerailizer(serializers.ModelSerializer):
    placed_at = serializers.DateTimeField(read_only=True)
    payment_status = serializers.CharField()
    items = OrderItemSerailizer(many=True)
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'items', 'placed_at', 'payment_status', 'user_id']

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    def validate_cart_id(self, cart_id):
        cart = Cart.objects.filter(id=cart_id).exists()
        if not cart:
            raise ValidationError('cart_id is not valid')
        return cart_id
    
    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            cart = Cart.objects.prefetch_related('items').get(id=cart_id)

            self.instance = order = Order.objects.create(
                user_id=self.context.get('user_id'),
            )

            orderitem = [OrderItem(
                order=order, product=cart_item.product, quantity=cart_item.quantity,
                unit_price=cart_item.product.unit_price) for cart_item in cart.items.all()
                ]

            products = []
            for cart_item in cart.items.all():
                product = cart_item.product
                product.inventory = F('inventory') - cart_item.quantity
                product.sold_number = F('sold_number') + cart_item.quantity
                products.append(product)
            Product.objects.bulk_update(products, ['inventory'])
            

            OrderItem.objects.bulk_create(orderitem)
            cart.delete()
            return self.instance


class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerailizer()
    product = ProductSerializer()
    class Meta:
        model = CartItem
        fields = ['order', 'product', 'quantity', 'unit_price']


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['title', 'description', 'product_set']