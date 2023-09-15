from model_bakery import baker
import pytest
from shop.models import CartItem
from rest_framework import status

@pytest.mark.django_db
class TestGetCartItem:
    def test_retrieving_returns_200(self, api_client):
        cart_item = baker.make(CartItem)

        response = api_client.get(f'/carts/{cart_item.cart.id}/items/{cart_item.id}/')

        assert response.status_code == status.HTTP_200_OK
    
    def test_listing_returns_200(self, api_client):
        cart_item = baker.make(CartItem)

        response = api_client.get(f'/carts/{cart_item.cart.id}/items/')

        assert response.status_code == status.HTTP_200_OK
    