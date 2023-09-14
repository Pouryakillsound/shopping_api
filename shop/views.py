import pprint

from django.db.models import F
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)
from django.utils.text import slugify
from rest_framework import permissions, status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   RetrieveModelMixin, UpdateModelMixin)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Cart, CartItem, Collection, Product, ProductImage
from .permissions import (CanAddImageToProductPermission,
                          CanCreateProductPermission,
                          CanEditImageRelatedToAProductPermission,
                          CanEditProductPermission, IsAdminOrReadOnly)
from .serializers import (CartSerializer, CollectionSerializer,
                          ProductAddSerializer,
                          ProductImageNestedToProductDetailSerializer,
                          ProductImageNestedToProductListSerializer,
                          ProductSerializer, ProductUpdateSerializer,
                          CartItemSerializer, CreateCartItemSerializer)


class MultipleLookupFields:
    def get_object(self):
        queryset = self.get_queryset()
        loopups = self.lookup_fields
        filters = {}
        for filter in loopups:
            filters[filter] = self.kwargs[filter]
        obj = get_object_or_404(queryset, **filters)
        self.check_object_permissions(self.request, obj)
        return obj


class ProductViewSet(MultipleLookupFields, ModelViewSet):
    http_method_names = ['header', 'options', 'get', 'patch', 'post', 'delete']
    queryset = Product.objects.prefetch_related('images', 'promotion').select_related('collection', 'seller').all()
    lookup_fields = ('pk', 'slug') #this field is optionally added by MultipleLookupFields class on the top,/
    #  be careful about changing this, cause then you should change urls as well

    def get_serializer_context(self):
        return {'request':self.request}

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'product': instance.get_absolute_url()})

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ProductSerializer
        elif self.request.method == 'PATCH':
            return ProductUpdateSerializer
        elif self.request.method == 'POST':
            return ProductAddSerializer

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [CanEditProductPermission()]
        elif self.request.method == 'POST':
            return [CanCreateProductPermission()]
        elif self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]


class ProductImageNestedToProductListView(ListCreateAPIView):

    serializer_class = ProductImageNestedToProductListSerializer
    lookups = ['product_pk'] #be careful about changing this, cause then you should change urls as well

    def get_queryset(self):
        queryset = ProductImage.objects.select_related('product')
        filters = {}
        for field in self.lookups:
            filters[field] = self.kwargs[field] 
        queryset = queryset.filter(product_id=filters['product_pk'])
        return queryset

    def get_serializer_context(self):
        return {'product_pk':self.kwargs['product_pk']}

    def get_permissions(self):
        if self.request.method == 'POST':
            return [CanAddImageToProductPermission()]
        return [AllowAny()]


class ProductImageNestedToProductDetailView(RetrieveUpdateDestroyAPIView):
    http_method_names = ['get', 'patch', 'delete', 'options', 'header']
    queryset = ProductImage.objects.select_related('product').all()
    serializer_class = ProductImageNestedToProductDetailSerializer
    
    def get_object(self):
        product_id = self.kwargs['product_pk']
        product_slug = self.kwargs['product_slug']
        pk = self.kwargs['image_pk']
        obj = get_object_or_404(ProductImage, pk=pk, product_id=product_id)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [CanEditImageRelatedToAProductPermission()]
        return [AllowAny()]

class CollectionViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    http_method_names = ['header', 'options', 'get', 'patch', 'post', 'delete']
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    http_method_names = ['get', 'patch', 'post', 'header', 'options']
    queryset = Cart.objects.prefetch_related('items__product__images').all()
    serializer_class = CartSerializer

    def create(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        seralizer = self.get_serializer(data=request.data)
        seralizer.is_valid(raise_exception=True)
        seralizer.save()
        return Response({'id': seralizer.data['id']}, status=status.HTTP_201_CREATED)

class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.select_related('cart', 'product')
    http_method_names = ['header', 'options', 'get', 'post', 'patch', 'delete']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cartitem = serializer.save()
        serializer = CartItemSerializer(cartitem)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return CreateCartItemSerializer
        elif self.request.method == 'GET':
            return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
