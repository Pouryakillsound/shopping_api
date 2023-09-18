import pytest
from shop.models import Collection, Product
from rest_framework import status
from model_bakery import baker

@pytest.fixture
def post_an_obj_to_collection(api_client, force_authenticate):
    def do_post_a_obj_to_collection(obj):
        force_authenticate(is_staff=True)
        response = api_client.post('/collections/', obj)
        return response
    return do_post_a_obj_to_collection
@pytest.fixture
def patch_an_obj_to_collection(api_client, force_authenticate):
    def do_patch_a_obj_to_collection(obj):
        collection = baker.make(Collection)
        force_authenticate(is_staff=True)
        response = api_client.patch(f'/collections/{collection.id}/', data=obj)
        return response
    return do_patch_a_obj_to_collection

@pytest.mark.django_db
class TestGetCollection:
    def test_get_list_returns_200(self, api_client):
        response = api_client.get('/collections/')
        
        assert response.status_code == status.HTTP_200_OK

    def test_get_detail_returns_200(self, api_client):

        collection = baker.make(Collection)
        respone = api_client.get(f'/collections/{collection.id}/')

        assert respone.status_code == status.HTTP_200_OK
    
    def test_if_object_does_not_exist_returns_404(self, api_client):
        response = api_client.get('/collections/1/')

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestPostCollection:
    def test_post_an_object_returns_201(self, post_an_obj_to_collection):
        response = post_an_obj_to_collection({
            'title': 'a'
        })

        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestPatchProduct:
    def test_patch_request_returns_200(self, patch_an_obj_to_collection):
        response = patch_an_obj_to_collection({'title': 'mamad'})

        assert response.status_code == status.HTTP_200_OK