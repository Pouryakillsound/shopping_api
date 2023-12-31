from model_bakery import baker
import pytest
from shop.models import CartItem, Cart, Product
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

    def test_if_object_does_not_exist_returns_404(self, api_client):
        response = api_client.get('/carts/92122adb-4d94-4890-9d5d-c3f6880e266b/items/1/')

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestPostCartItem:
    def test_post_returns_201(self, api_client):
        cart = baker.make(Cart)
        product = baker.make(Product)

        response = api_client.post(f'/carts/{cart.id}/items/', {'product_id': product.id, 'quantity': 1})

        assert response.status_code == status.HTTP_201_CREATED

    def test_creating_a_existing_cartitem_only_increases_the_quantity_of_existing_one(self, api_client):
        product = baker.make(Product, inventory=10000)
        cart_item = baker.make(CartItem, product=product, quantity=1)
        existing_quantity = cart_item.quantity
        quantity = 1

        response = api_client.post(f'/carts/{cart_item.cart.id}/items/', {'product_id': cart_item.product.id, 'quantity': quantity})

        assert response.data['quantity'] == quantity + existing_quantity

@pytest.mark.django_db
class TestPatchCartItem:
    def test_patch_returns_200_and_correct_data(self, api_client):
        cart_item = baker.make(CartItem)
        product = baker.make(Product)
        response = api_client.patch(f'/carts/{cart_item.cart.id}/items/{cart_item.id}/', {'product_id':product.id, 'quantity': 1})

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'product_id': product.id, 'quantity': 1}

@pytest.mark.django_db
class TestDeleteCartItem:
    def test_delete_returns_204(self, api_client):
        cart_item = baker.make(CartItem)

        response = api_client.delete(f'/carts/{cart_item.cart.id}/items/{cart_item.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT