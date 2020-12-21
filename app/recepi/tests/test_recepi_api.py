from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recepi

from recepi.serializers import RecepiSerializer

RECEPIS_URL = reverse('recepi:recepi-list')


def sample_recipe(user, **params):
    """create adn return a sample recipe"""
    defaults = {
        'title': 'Sample_recepi',
        'time_minutes': 10,
        'price': 5.00
    }
    defaults.update(params)

    return Recepi.objects.create(user=user, **defaults)


class PublicRecepiApiTests(TestCase):
    """Test unanthenticated recepi API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """TEst tha authentication is required"""
        res = self.client.get(RECEPIS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTEst(TestCase):
    """TEst unauthenticated recepi API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'te4s134'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """test retrieving a list of recepis"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECEPIS_URL)

        recipes = Recepi.objects.all().order_by('-id')
        serializer = RecepiSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """TEst retrieven recipes for current user"""
        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'pass132'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECEPIS_URL)

        recipes = Recepi.objects.filter(user=self.user)
        serializer = RecepiSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)