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
    prepopulated_fields = {'slug':['title']}
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
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['title']}
    fields = ['title', 'description', 'slug', 'inventory', 'unit_price', 'collection']
    list_display = ['title', 'low_inventory', 'unit_price']
    list_editable = ['unit_price']
    search_fields = ['title']
    list_filter = [LowProductInventoryFilter]

    @admin.display(description='inventory', ordering='inventory')
    def low_inventory(self, product):
        if product.inventory <= 10:
            return 'LOW'
        return product.inventory



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['order', 'product', 'quantity', 'unit_price']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ['user','payment_status']
    list_display = ['user', 'payment_status', 'placed_at']
    list_filter = ['payment_status']
    search_fields = ['user']
    inlines = [OrderItemInline]



@admin.register(OrderItem)
class OrderItem(admin.ModelAdmin):
    fields = ['order', 'product', 'quantity', 'unit_price']
    list_display = ['order', 'product', 'quantity']
    search_fields = ['order__user__username']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'created_at']
    list_display = ['id', 'created_at']
    search_fields = ['id']


@admin.register(CartItem)
class CartItem(admin.ModelAdmin):
    fields = ['cart', 'product', 'quantity']
    autocomplete_fields = ['cart', 'product']
    list_display = ['cart', 'product', 'quantity']
    search_fields = ['cart__id', 'product__title']