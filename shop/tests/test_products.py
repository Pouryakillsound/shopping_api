from decimal import Decimal
import pytest
from shop.models import Product
from model_bakery import baker
from account.models import User
from rest_framework import status
from shop.models import Collection, Product


@pytest.fixture
def post_to_product(api_client):
    def do_post_to_product(data):
        
        url = '/products/'
        response = api_client.post(url, data)
        return response
    return do_post_to_product


@pytest.fixture
def patch_to_product(api_client, force_authenticate_with_perm):
    def do_patch_product(data):
        force_authenticate_with_perm('can edit product', is_staff=True)
        product = baker.make(Product, seller_id=1)
        url = f'/products/{product.id}/{product.slug}/'
        response = api_client.patch(url, data)
        return response
    return do_patch_product


@pytest.mark.django_db
class TestGetProuct:

    def test_products_list_url_return_200(self, api_client):

        response = api_client.get('/products/')
        
        assert response.status_code == status.HTTP_200_OK

    def test_products_detail_url_return_200(self, api_client):
        product = baker.make('shop.Product')

        response = api_client.get(f'/products/{product.id}/{product.slug}/')

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCreateProduct:

    def test_with_posting_a_product_returns_201(self, force_authenticate_with_perm, post_to_product):
        baker.make(Collection, id=1)

        force_authenticate_with_perm('Can add product', is_staff=True)
        response = post_to_product(data={
        "title": "a",
        "description": "a",
        "inventory": 10,
        "unit_price": 10,
        "collection_id": 1
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {
        "title": "a",
        "description": "a",
        "inventory": 10,
        "unit_price": "10.00",
        "collection_id": 1,
        }


@pytest.mark.django_db
class TestPatchProduct:
    def test_patch_returns_200(self, patch_to_product):
        response = patch_to_product({'title': 'a'})

        assert response.status_code == status.HTTP_200_OK
