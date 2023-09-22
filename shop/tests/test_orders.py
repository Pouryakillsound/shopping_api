from rest_framework import status
import pytest

@pytest.mark.django_db
class TestGetOrder:
    def test_getting_list_returns_200(self, api_client, force_authenticate):
        force_authenticate(is_staff=False)
        response = api_client.get('/orders/')
        assert response.status_code == status.HTTP_200_OK