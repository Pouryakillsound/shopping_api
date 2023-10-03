from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from .models import UserProfile, Address
from .serializers import UserProfileSerilizer, AddressSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


class UserProfileView(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserProfileSerilizer
    def get_object(self):
        obj = get_object_or_404(UserProfile, user_id=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj

class AddressViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer
    def get_queryset(self):
        if self.request.user.is_staff:
            return Address.objects.all()
        else:
            return Address.objects.filter(customer_id=self.request.user.id)
    def get_serializer_context(self):
        return {'customer_Id': self.request.user.id}
