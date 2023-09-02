from django.shortcuts import get_object_or_404, render
from rest_framework.viewsets import ModelViewSet
from .models import Product
from .serializers import ProductSerializer
from rest_framework import status

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
    http_method_names = ['header', 'options', 'get', 'patch', 'post']
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_fields = ('pk', 'slug') #this field is optionally added by MultipleLookupFields class on the top

