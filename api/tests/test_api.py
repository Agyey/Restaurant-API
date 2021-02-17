from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient, Cuisine, Dish, Menu, Restaurant
from core.serializers import (
    IngredientSerializer,
    CuisineSerializer,
    DishSerializer,
    MenuSerializer,
    RestaurantSerializer,
)


class TestIngredientAPI(TestCase):
    """Test Ingredient API"""

    def setUp(self):
        self.staff_user = get_user_model().objects.create_superuser(
            email="abc@test.com", password="password123",
        )
        self.user = get_user_model().objects.create_user(
            email="xyz@test.com", password="password123",
        )
        self.client = APIClient()
        self.salt = Ingredient.objects.create(name="Salt", price="0.5")

    def test_view_ingredient_list(self):
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        url = reverse("ingredient-list")
        self.client.force_authenticate(user=self.user)
        res = self.client.get(url)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.get(url)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_view_valid_ingredient_detail(self):
        pk = self.salt.pk
        ingredients = Ingredient.objects.get(pk=pk)
        serializer = IngredientSerializer(ingredients)
        url = reverse("ingredient-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.get(url)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.get(url)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_view_invalid_ingredient_detail(self):
        pk = 1234
        url = reverse("ingredient-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_ingredient(self):
        payload = {
            "name": "honey",
            "price": 5,
        }
        url = reverse("ingredient-list")
        self.client.force_authenticate(user=self.user)
        res = self.client.post(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.post(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_ingredient(self):
        payload = {
            "name": "",
            "price": 5,
        }
        url = reverse("ingredient-list")
        self.client.force_authenticate(user=self.user)
        res = self.client.post(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.post(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_update_ingredient(self):
        pk = self.salt.pk
        payload = {
            "name": "honey",
            "price": 5,
        }
        url = reverse("ingredient-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.put(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.put(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], payload["name"])
        self.assertEqual(res.data["price"], float(payload["price"]))

    def test_invalid_update_ingredient(self):
        pk = self.salt.pk
        payload = {
            "price": "1",
        }
        url = reverse("ingredient-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.put(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.put(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_patch_ingredient(self):
        pk = self.salt.pk
        payload = {
            "price": "1",
        }
        url = reverse("ingredient-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.patch(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.patch(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["price"], float(payload["price"]))

    def test_valid_delete_ingredient(self):
        pk = self.salt.pk
        url = reverse("ingredient-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_ingredient(self):
        pk = 1234
        url = reverse("ingredient-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class TestCuisineAPI(TestCase):
    def setUp(self):
        self.staff_user = get_user_model().objects.create_superuser(
            email="abc@test.com", password="password123",
        )
        self.user = get_user_model().objects.create_user(
            email="xyz@test.com", password="password123",
        )
        self.client = APIClient()
        self.salt = Ingredient.objects.create(name="Salt", price="0.5")
        self.pepper = Ingredient.objects.create(name="Pepper", price="0.4")
        self.egg = Ingredient.objects.create(name="Egg", price="1")
        self.continental = Cuisine.objects.create(
            name="continental", origin="world"
        )
        self.continental.popular_ingredients.add(
            self.salt, self.pepper, self.egg
        )

    def test_view_cuisine_list(self):
        cuisines = Cuisine.objects.all()
        serializer = CuisineSerializer(cuisines, many=True)
        url = reverse("cuisine-list")
        self.client.force_authenticate(user=self.user)
        res = self.client.get(url)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.get(url)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_view_valid_cuisine_detail(self):
        pk = self.continental.pk
        cuisines = Cuisine.objects.get(pk=pk)
        serializer = CuisineSerializer(cuisines)
        url = reverse("cuisine-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.get(url)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.get(url)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_view_invalid_cuisine_detail(self):
        pk = 1234
        url = reverse("cuisine-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_cuisine(self):
        payload = {
            "name": "Asian",
            "origin": "South-East Asia",
            "popular_ingredients": [self.salt.pk, self.pepper.pk, self.egg.pk],
        }
        url = reverse("cuisine-list")
        self.client.force_authenticate(user=self.user)
        res = self.client.post(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.post(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_cuisine(self):
        payload = {
            "name": "",
            "origin": "South-East Asia",
            "popular_ingredients": [self.salt.pk, self.pepper.pk, self.egg.pk],
        }
        url = reverse("cuisine-list")
        self.client.force_authenticate(user=self.user)
        res = self.client.post(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.post(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_update_cuisine(self):
        pk = self.continental.pk
        payload = {
            "name": "Continental",
            "origin": "Europe",
            "popular_ingredients": [self.salt.pk, self.pepper.pk, self.egg.pk],
        }
        url = reverse("cuisine-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.put(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.put(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], payload["name"])
        self.assertEqual(res.data["origin"], payload["origin"])
        self.assertEqual(
            res.data["popular_ingredients"], payload["popular_ingredients"]
        )

    def test_invalid_update_cuisine(self):
        pk = self.continental.pk
        payload = {
            "name": "Continental",
        }
        url = reverse("cuisine-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.put(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.put(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_patch_cuisine(self):
        pk = self.continental.pk
        payload = {
            "origin": "Europe",
        }
        url = reverse("cuisine-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.patch(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.patch(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["origin"], payload["origin"])

    def test_valid_delete_cuisine(self):
        pk = self.continental.pk
        url = reverse("cuisine-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_cuisine(self):
        pk = 1234
        url = reverse("cuisine-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class TestDishAPI(TestCase):
    """Test Dish API"""

    def setUp(self):
        self.staff_user = get_user_model().objects.create_superuser(
            email="abc@test.com", password="password123",
        )
        self.user = get_user_model().objects.create_user(
            email="xyz@test.com", password="password123",
        )
        self.client = APIClient()
        self.salt = Ingredient.objects.create(name="Salt", price="0.5")
        self.pepper = Ingredient.objects.create(name="Pepper", price="0.4")
        self.egg = Ingredient.objects.create(name="Egg", price="1")
        self.continental = Cuisine.objects.create(
            name="continental", origin="world"
        )
        self.continental.popular_ingredients.add(
            self.salt, self.pepper, self.egg
        )
        self.omelette = Dish.objects.create(
            name="Omelette", serves=1, price=3,
        )
        self.omelette.ingredients.add(self.salt, self.pepper, self.egg)
        self.omelette.cuisine = self.continental

    def test_view_dish_list(self):
        dishes = Dish.objects.all()
        serializer = DishSerializer(dishes, many=True)
        url = reverse("dish-list")
        self.client.force_authenticate(user=self.user)
        res = self.client.get(url)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.get(url)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_view_valid_dish_detail(self):
        pk = self.omelette.pk
        dish = Dish.objects.get(pk=pk)
        serializer = DishSerializer(dish)
        url = reverse("dish-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.get(url)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.get(url)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_view_invalid_dish_detail(self):
        pk = 1234
        url = reverse("dish-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_dish(self):
        payload = {
            "ingredients": [self.salt.pk, self.pepper.pk, self.egg.pk],
            "name": "Omelette",
            "price": 3,
            "serves": 1,
            "cuisine": self.continental.pk,
        }
        url = reverse("dish-list")
        self.client.force_authenticate(user=self.user)
        res = self.client.post(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.post(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_dish(self):
        payload = {
            "name": "",
            "price": 5,
        }
        url = reverse("dish-list")
        self.client.force_authenticate(user=self.user)
        res = self.client.post(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.post(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_update_dish(self):
        pk = self.omelette.pk
        payload = {
            "ingredients": [self.salt.pk, self.pepper.pk, self.egg.pk],
            "name": "Omelette",
            "price": 5,
            "serves": 1,
            "cuisine": self.continental.pk,
        }
        url = reverse("dish-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.put(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.put(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], payload["name"])
        self.assertEqual(res.data["ingredients"], payload["ingredients"])
        self.assertEqual(res.data["serves"], payload["serves"])
        self.assertEqual(res.data["cuisine"], payload["cuisine"])
        self.assertEqual(res.data["price"], float(payload["price"]))

    def test_invalid_update_dish(self):
        pk = self.omelette.pk
        payload = {
            "price": "1",
        }
        url = reverse("dish-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.put(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.put(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_patch_dish(self):
        pk = self.omelette.pk
        payload = {
            "price": "5",
        }
        url = reverse("dish-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.patch(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.patch(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["price"], float(payload["price"]))

    def test_valid_delete_dish(self):
        pk = self.omelette.pk
        url = reverse("dish-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_dish(self):
        pk = 1234
        url = reverse("dish-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class TestRestaurantAPI(TestCase):
    """Test Restaurant API"""

    def setUp(self):
        self.staff_user = get_user_model().objects.create_superuser(
            email="abc@test.com", password="password123",
        )
        self.user = get_user_model().objects.create_user(
            email="xyz@test.com", password="password123",
        )
        self.client = APIClient()
        self.salt = Ingredient.objects.create(name="Salt", price="0.5")
        self.pepper = Ingredient.objects.create(name="Pepper", price="0.4")
        self.egg = Ingredient.objects.create(name="Egg", price="1")
        self.continental = Cuisine.objects.create(
            name="continental", origin="world"
        )
        self.continental.popular_ingredients.add(
            self.salt, self.pepper, self.egg
        )
        self.omelette = Dish.objects.create(
            name="Omelette", serves=1, price=3,
        )
        self.omelette.ingredients.add(self.salt, self.pepper, self.egg)
        self.omelette.cuisine = self.continental
        self.restaurant = Restaurant.objects.create(
            name="Agyey's Kitchen",
            owner="Agyey Arya",
            location="Delhi NCR, India",
            email="agyey@test.com",
            contact_number="+00000000000",
            website="agyeyskitchen.in",
        )

    def test_view_restaurant_list(self):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        url = reverse("restaurant-list")
        self.client.force_authenticate(user=self.user)
        res = self.client.get(url)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.get(url)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_view_valid_restaurant_detail(self):
        pk = self.restaurant.pk
        restaurant = Restaurant.objects.get(pk=pk)
        serializer = RestaurantSerializer(restaurant)
        url = reverse("restaurant-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.get(url)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.get(url)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_view_invalid_restaurant_detail(self):
        pk = 1234
        url = reverse("restaurant-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_restaurant(self):
        payload = {
            "name": "Agyey's Kitchen",
            "owner": "Agyey Arya",
            "established": "1997-11-27",
            "location": "Delhi NCR, India",
            "email": "agyey@test.com",
            "contact_number": "+00000000000",
            "website": "https://www.agyeyskitchen.in",
        }
        url = reverse("restaurant-list")
        self.client.force_authenticate(user=self.user)
        res = self.client.post(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.post(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_restaurant(self):
        payload = {
            "name": "",
            "owner": "Agyey Arya",
            "location": "Delhi NCR, India",
            "email": "agyey@test.com",
            "contact_number": "+00000000000",
            "website": "https://www.agyeyskitchen.in",
        }
        url = reverse("restaurant-list")
        self.client.force_authenticate(user=self.user)
        res = self.client.post(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.post(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_update_restaurant(self):
        pk = self.restaurant.pk
        payload = {
            "name": "Agyey's Kitchen",
            "owner": "Agyey Arya",
            "established": "1997-11-27",
            "location": "Delhi NCR, India",
            "email": "agyey@test.com",
            "contact_number": "+00000000000",
            "website": "https://www.agyeyskitchen.in",
        }
        url = reverse("restaurant-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.put(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.put(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], payload["name"])
        self.assertEqual(res.data["owner"], payload["owner"])
        self.assertEqual(res.data["established"], payload["established"])
        self.assertEqual(res.data["location"], payload["location"])
        self.assertEqual(res.data["email"], payload["email"])
        self.assertEqual(res.data["contact_number"], payload["contact_number"])
        self.assertEqual(res.data["contact_number"], payload["contact_number"])

    def test_invalid_update_restaurant(self):
        pk = self.restaurant.pk
        payload = {
            "price": "1",
        }
        url = reverse("restaurant-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.put(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.put(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_patch_restaurant(self):
        pk = self.restaurant.pk
        payload = {
            "established": "1997-11-27",
        }
        url = reverse("restaurant-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.patch(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.patch(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["established"], payload["established"])

    def test_valid_delete_restaurant(self):
        pk = self.restaurant.pk
        url = reverse("restaurant-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_restaurant(self):
        pk = 1234
        url = reverse("restaurant-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class TestMenuAPI(TestCase):
    """Test Menu API"""

    def setUp(self):
        self.staff_user = get_user_model().objects.create_superuser(
            email="abc@test.com", password="password123",
        )
        self.user = get_user_model().objects.create_user(
            email="xyz@test.com", password="password123",
        )
        self.client = APIClient()
        self.salt = Ingredient.objects.create(name="Salt", price="0.5")
        self.pepper = Ingredient.objects.create(name="Pepper", price="0.4")
        self.egg = Ingredient.objects.create(name="Egg", price="1")
        self.continental = Cuisine.objects.create(
            name="continental", origin="world"
        )
        self.continental.popular_ingredients.add(
            self.salt, self.pepper, self.egg
        )
        self.omelette = Dish.objects.create(
            name="Omelette", serves=1, price=3,
        )
        self.omelette.ingredients.add(self.salt, self.pepper, self.egg)
        self.omelette.cuisine = self.continental
        self.restaurant = Restaurant.objects.create(
            name="Agyey's Kitchen",
            owner="Agyey Arya",
            location="Delhi NCR, India",
            email="agyey@test.com",
            contact_number="+00000000000",
            website="agyeyskitchen.in",
        )
        self.menu = Menu.objects.create(restaurant=self.restaurant)
        self.menu.dishes.add(self.omelette)
        self.menu.cuisines.add(self.continental)

    def test_view_menu_list(self):
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        url = reverse("menu-list")
        self.client.force_authenticate(user=self.user)
        res = self.client.get(url)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.get(url)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_view_valid_menu_detail(self):
        pk = self.menu.pk
        menu = Menu.objects.get(pk=pk)
        serializer = MenuSerializer(menu)
        url = reverse("menu-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.get(url)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.get(url)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_view_invalid_menu_detail(self):
        pk = 1234
        url = reverse("menu-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_menu(self):
        payload = {
            "restaurant": self.restaurant.pk,
            "cuisines": [self.continental.pk],
            "dishes": [self.omelette.pk],
        }
        url = reverse("menu-list")
        self.client.force_authenticate(user=self.user)
        res = self.client.post(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.post(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_menu(self):
        payload = {
            "restaurant": 1234,
            "cuisines": [self.continental.pk],
            "dishes": [self.omelette.pk],
        }
        url = reverse("menu-list")
        self.client.force_authenticate(user=self.user)
        res = self.client.post(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.post(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_update_menu(self):
        pk = self.menu.pk
        payload = {
            "restaurant": self.restaurant.pk,
            "cuisines": [],
            "dishes": [self.omelette.pk],
        }
        url = reverse("menu-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.put(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.put(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["restaurant"], payload["restaurant"])
        self.assertEqual(res.data["cuisines"], payload["cuisines"])
        self.assertEqual(res.data["dishes"], payload["dishes"])

    def test_invalid_update_menu(self):
        pk = self.menu.pk
        payload = {
            "price": "1",
        }
        url = reverse("menu-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.put(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.put(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_patch_menu(self):
        pk = self.menu.pk
        payload = {
            "cuisines": [],
        }
        url = reverse("menu-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.patch(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.patch(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data["cuisines"],
            [cuisine.pk for cuisine in self.menu.cuisines.all()],
        )

    def test_valid_delete_menu(self):
        pk = self.menu.pk
        url = reverse("menu-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_menu(self):
        pk = 1234
        url = reverse("menu-detail", args=[pk])
        self.client.force_authenticate(user=self.user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.staff_user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
