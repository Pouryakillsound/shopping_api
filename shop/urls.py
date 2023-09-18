from pprint import pprint

from django.urls import path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from .views import (CartItemViewSet, CartViewSet, CollectionViewSet,
                    ProductImageNestedToProductDetailView,
                    ProductImageNestedToProductListView, ProductViewSet, OrderViewSet)

app_name = 'shop'

router = DefaultRouter()
product = router.register('products', ProductViewSet, basename='products')
order = router.register('orders', OrderViewSet, basename='orders')
router.register('collections', CollectionViewSet, basename='collections')
router.register('carts', CartViewSet)
cartitem_router = NestedDefaultRouter(router, 'carts', lookup='cart')
cartitem_router.register('items', CartItemViewSet, basename='cartitems')



urlpatterns = [
    path('products/<int:pk>/<slug:slug>/',
        ProductViewSet.as_view({'get':'retrieve', 'patch':'partial_update', 'delete':'destroy'}),
        name='products-detail-with-slug'),
    path('products/<int:product_pk>/<slug:product_slug>/images/',
          ProductImageNestedToProductListView.as_view(), name='product-images-list'),
    path('products/<int:product_pk>/<slug:product_slug>/images/<int:image_pk>/',
          ProductImageNestedToProductDetailView.as_view(), name='product-images-list')
    ]

urlpatterns += router.urls + cartitem_router.urls
