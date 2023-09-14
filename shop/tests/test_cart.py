from model_bakery import baker
from shop.models import Cart
from rest_framework import status
import pytest


@pytest.mark.django_db
class TestGetCart:
    def test_retrieve_returns_200(self, api_client):
        cart = baker.make(Cart)
        response = api_client.get(f'/carts/{cart.id}/')


        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestPostCart:
    def test_post_returns_201(self, api_client):
        response = api_client.post('/carts/', {})

        assert response.status_code == status.HTTP_201_CREATED
