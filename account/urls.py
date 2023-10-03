from django.urls import path
from .views import UserProfileView, AddressViewSet
from rest_framework.routers import DefaultRouter

app_name='account'
router = DefaultRouter()
router.register('addresses', AddressViewSet, basename='address')

urlpatterns = [
    path('profile/', UserProfileView.as_view({'get':'retrieve', 'patch':'update'}), name='profile-detail')
]
urlpatterns += router.urls