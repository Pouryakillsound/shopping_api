import pytest
from shop.models import Collection
from rest_framework import status
from model_bakery import baker

@pytest.fixture
def post_an_obj_to_collection(api_client, force_authenticate):
    def do_post_a_obj_to_collection(obj):
        force_authenticate(is_staff=True)
        response = api_client.post('/collections/', obj)
        return response
    return do_post_a_obj_to_collection
    


@pytest.mark.django_db
class TestGetCollection:
    def test_get_list_returns_200(self, api_client):
        response = api_client.get('/collections/')
        
        assert response.status_code == status.HTTP_200_OK

    def test_get_detail_returns_200(self, api_client):

        collection = baker.make(Collection)
        respone = api_client.get(f'/collections/{collection.id}/')

        assert respone.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestPostCollection:
    def test_post_an_object_returns_201(self, post_an_obj_to_collection):
        response = post_an_obj_to_collection({
            'title': 'a'
        })

        assert response.status_code == status.HTTP_201_CREATED