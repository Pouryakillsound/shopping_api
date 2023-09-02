from rest_framework.routers import DefaultRouter
from .views import ProductViewSet
from pprint import pprint
from django.urls import path
router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')


urlpatterns = [path('products/<int:pk>/<slug:slug>/', ProductViewSet.as_view({'get':'retrieve', 'patch':'partial_update'}), name='products-detail')] + router.urls

pprint(router.urls)