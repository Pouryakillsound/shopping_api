from django.shortcuts import get_object_or_404, render
from rest_framework.reverse import reverse_lazy
from rest_framework.viewsets import ModelViewSet
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer
from rest_framework import status
from django.shortcuts import redirect
from django.utils.text import slugify
from rest_framework.response import Response


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
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        new_url = reverse_lazy('shop:products-detail-with-slug', [instance.id, instance.slug])
        return Response({'product': new_url})

    #permission should be added
    http_method_names = ['header', 'options', 'get', 'patch', 'post']
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_fields = ('pk', 'slug') #this field is optionally added by MultipleLookupFields class on the top


class CollectionViewSet(ModelViewSet):
    #permission should be added
    http_method_names = ['header', 'options', 'get', 'patch', 'post']
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    lookup_field = 'title'