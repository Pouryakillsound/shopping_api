from rest_framework import serializers
from .models import UserProfile, Address
from .models import User
from django.core.exceptions import ValidationError



class AddressSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Address
        fields = ['id', 'city', 'street', 'district', 'zipcode', 'unit', 'customer_id']
    
    def create(self, validated_data):
        customer_Id = self.context['customer_Id']
        user_profile = UserProfile.objects.get(user_id=customer_Id)
        address = Address.objects.create(customer_id=user_profile.id, **validated_data)
        return address

class UserProfileSerilizer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['user', 'age', 'national_code']
