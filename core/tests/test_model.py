from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTest(TestCase):
    """Test for User Model creation and modification"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with email is successful"""
        email = "abc@xyz.com"
        password = "password@123"
        user = get_user_model().objects.create_user(
            email=email, password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email for new user is normalized"""
        email = "abc@XYZ.com"
        password = "password@123"
        user = get_user_model().objects.create_user(
            email=email, password=password,
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None, password="password@123",
            )

    def test_create_new_superuser(self):
        """Test creating a new super user"""
        email = "abc@XYZ.com"
        password = "password@123"
        user = get_user_model().objects.create_superuser(
            email=email, password=password,
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
