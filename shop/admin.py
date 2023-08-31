from typing import Any, List, Optional, Tuple
from django.contrib import admin
from django.db.models.query import QuerySet
from django.forms import Textarea
from .models import Product, Collection, Cart, CartItem, Order, OrderItem
from django.db import models


class LowProductInventoryFilter(admin.SimpleListFilter):
    title = 'Low Inventory'
    parameter_name = 'Low'
    def lookups(self, request: Any, model_admin: Any):
        return [
            ('<10', 'Low')
        ]
    
    def queryset(self, request: Any, queryset: QuerySet[Any]):
        if self.value() == '<10':
            return queryset.filter(inventory__lte=10)
        
class ProductInline(admin.TabularInline):
    model=Product
    fields = ['title', 'description', 'inventory', 'unit_price', 'collection']
    extra = 1
    formfield_overrides = {
        models.TextField:{'widget': Textarea(attrs={'rows':3, 'cols':40})}
    }


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    model = Collection
    fields = ['title']
    inlines = [ProductInline]
    search_fields = ['title']


@admin.register(Product)
class ProductAdmib(admin.ModelAdmin):
    model = Product
    fields = ['title', 'description', 'inventory', 'unit_price', 'collection']
    list_display = ['title', 'low_inventory', 'unit_price']
    list_editable = ['unit_price']
    search_fields = ['title']
    list_filter = [LowProductInventoryFilter]

    @admin.display(ordering='inventory')
    def low_inventory(self, product):
        if product.inventory <= 10:
            return 'LOW'
        return product.inventory



admin.site.register(Order)
admin.site.register(OrderItem)