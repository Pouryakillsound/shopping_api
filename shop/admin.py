from django.contrib import admin
from django.forms import Textarea
from .models import Product, Collection
from django.db import models
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
    list_display = ['title', 'inventory', 'unit_price']
    list_editable = ['unit_price']
    search_fields = ['title']
