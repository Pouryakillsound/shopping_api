from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CollectionViewSet
from pprint import pprint
from django.urls import path

app_name = 'shop'

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('collections', CollectionViewSet, basename='collections')


urlpatterns = [
    path('products/<int:pk>/<slug:slug>/',
        ProductViewSet.as_view({'get':'retrieve', 'patch':'partial_update'}),
        name='products-detail-with-slug')
    ]

urlpatterns += router.urls
