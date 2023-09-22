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
    def test_if_object_does_not_exist_returns_404(self, api_client):
        response = api_client.get('/carts/92122adb-4d94-4890-9d5d-c3f6880e266b/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestPostCart:
    def test_post_returns_201(self, api_client):
        response = api_client.post('/carts/', {})

        assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
class TestDeleteCart:
    def test_delete_returns_204(self, api_client):
        cart = baker.make(Cart)

        response = api_client.delete(f'/carts/{cart.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT