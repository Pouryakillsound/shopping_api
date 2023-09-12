import pytest
from rest_framework.test import APIClient
from account.models import User
from django.contrib.auth.models import Permission

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def force_authenticate(api_client):
    def do_force_authenticate(is_staff=False):
        user = api_client.force_authenticate(user=User(is_staff=is_staff))
        return user
    return do_force_authenticate


@pytest.fixture
def force_authenticate_with_perm(api_client):
    def do_force_authenticate_with_perm(permission_name, is_staff=False):
        user = User(id=1, is_staff=is_staff)
        user.save()
        perm = Permission.objects.get(name=permission_name)
        user.user_permissions.add(perm)
        root = api_client.force_authenticate(user=user)
        return root
    return do_force_authenticate_with_perm