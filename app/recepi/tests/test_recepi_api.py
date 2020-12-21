from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recepi, Tag, Ingredient

from recepi.serializers import RecepiSerializer, RecepiDetailSerializer

RECEPIS_URL = reverse('recepi:recepi-list')


def detail_url(recepi_id):
    """Return recepi detail URL"""
    return reverse('recepi:recepi-detail', args=[recepi_id])


def sample_tag(user, name='Main Course'):
    """Create and return a sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='Cinnamon'):
    """create and return a sample ingredient"""
    return Ingredient.objects.create(user=user, name=name)


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

    def test_view_recepi_detail(self):
        """test viewing a recipe detail"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecepiDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_recepi(self):
        """test creating recepi"""
        payload = {
            'title': 'Chocolate cheesecake',
            'time_minutes': 30,
            'price': 5.00
        }
        res = self.client.post(RECEPIS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recepi.objects.get(id = res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recepi_with_tags(self):
        """test creating a recipe with tag"""
        tag1 = sample_tag(user=self.user, name='Vegan')
        tag2 = sample_tag(user=self.user, name='dessert')
        payload = {
            'title': 'Avocado lime cheesecake',
            'tags': [tag1.id, tag2.id],
            'time_minutes': 60,
            'price': 20.00
        }
        res = self.client.post(RECEPIS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recepi.objects.get(id=res.data['id'])
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_recepi_with_ingredient(self):
        """test creating recepi with ingredients"""
        ingredient1 = sample_ingredient(user=self.user, name='Prawns')
        ingredient2 = sample_ingredient(user=self.user, name='Ginger')
        payload = {
            'title': 'Thai prawn red curry',
            'ingredients': [ingredient1.id, ingredient2.id],
            'time_minutes': 20,
            'price':7.00
        }
        res = self.client.post(RECEPIS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recepi.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)
