from .views import ProductViewSet, CollectionViewSet, ProductImageView
from pprint import pprint
from django.urls import path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

app_name = 'shop'

router = DefaultRouter()
product = router.register('products', ProductViewSet, basename='products')
product_nested = NestedDefaultRouter(router, 'products')
product_nested.register('images', ProductImageView, basename='product-images')
router.register('collections', CollectionViewSet, basename='collections')



urlpatterns = [
    path('products/<int:pk>/<slug:slug>/',
        ProductViewSet.as_view({'get':'retrieve', 'patch':'partial_update', 'delete':'destroy'}),
        name='products-detail-with-slug'),
    path('products/<int:id>/<slug:slug>/images', ProductImageView.as_view({'get':'list', 'post':'create'}), name='product-images-list')
    ]

urlpatterns += router.urls + product_nested.urls
