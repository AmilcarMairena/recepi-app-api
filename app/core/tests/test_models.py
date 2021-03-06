from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='prueba@gmail.com', password='prueba123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'prueba@gmail.com'
        password = 'pruebapass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        """Test the email for a new user is normalized"""
        email = 'prueba@GMAIL.COM'
        user = get_user_model().objects.create_user(email, 'prueba123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """TEst creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'prueba123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'prueba@gmail.com',
            'prueba123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user = sample_user(),
            name = 'vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_model(self):
        """test the ingrediant string representation"""
        ingredient = models.Ingredient.objects.create(
            user = sample_user(),
            name = 'cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recepi_str(self):
        """Test the recepi string representation"""
        recepi = models.Recepi.objects.create(
            user = sample_user(),
            title='Steak and mishroon souce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recepi), recepi.title)
