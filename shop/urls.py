from .views import ProductViewSet, CollectionViewSet, ProductImageNestedToProductListView, ProductImageNestedToProductDetailView
from pprint import pprint
from django.urls import path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

app_name = 'shop'

router = DefaultRouter()
product = router.register('products', ProductViewSet, basename='products')
router.register('collections', CollectionViewSet, basename='collections')



urlpatterns = [
    path('products/<int:pk>/<slug:slug>/',
        ProductViewSet.as_view({'get':'retrieve', 'patch':'partial_update', 'delete':'destroy'}),
        name='products-detail-with-slug'),
    path('products/<int:product_pk>/<slug:product_slug>/images/',
          ProductImageNestedToProductListView.as_view(), name='product-images-list'),
    path('products/<int:product_pk>/<slug:product_slug>/images/<int:image_pk>/',
          ProductImageNestedToProductDetailView.as_view(), name='product-images-list')
    ]

urlpatterns += router.urls