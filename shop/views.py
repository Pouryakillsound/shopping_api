from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from rest_framework import permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .models import Collection, Product, ProductImage, Cart
from .permissions import (CanCreateProductPermission, CanEditProductPermission,
                          IsAdminOrReadOnly, CanAddImageToProduct)
from .serializers import (CollectionSerializer, ProductAddSerializer,
                          ProductSerializer, ProductUpdateSerializer, ProductImageNestedToProductListSerializer, ProductImageNestedToProductDetailSerializer)

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
    queryset = Product.objects.prefetch_related('images', 'promotion').select_related('collection').all()
    lookup_fields = ('pk', 'slug') #this field is optionally added by MultipleLookupFields class on the top, be careful about changing this, cause then you should change urls as well

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
    queryset = ProductImage.objects.select_related('product').all()
    serializer_class = ProductImageNestedToProductListSerializer
    lookups = ['product_pk', 'product_slug'] #be careful about changing this, cause then you should change urls as well

    def get_object(self):
        queryset = self.get_queryset()
        lookups = self.lookups
        filters = {}
        for field in lookups:
            filters[field] = self.kwargs[field]
        obj = queryset.filter(filters)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_context(self):
        return {'product_pk':self.kwargs['product_pk']}

    def get_permissions(self):
        if self.request.method == 'POST':
            return [CanAddImageToProduct()]
        return [AllowAny()]


class ProductImageNestedToProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.select_related('product').all()
    serializer_class = ProductImageNestedToProductDetailSerializer

    def get_object(self):
        product_id = self.kwargs['product_pk']
        product_slug = self.kwargs['product_slug']
        pk = self.kwargs['image_pk']
        obj = get_object_or_404(ProductImage, pk=pk, product_id=product_id)
        self.check_object_permissions(self.request, obj)
        return obj


class CollectionViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    http_method_names = ['header', 'options', 'get', 'patch', 'post', 'delete']
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    lookup_field = 'title'

