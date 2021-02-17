from rest_framework import serializers

from core import models


class IngredientSerializer(serializers.ModelSerializer):
    """Serializes Ingredient"""

    class Meta:
        model = models.Ingredient
        fields = ("id", "name", "price")


class CuisineSerializer(serializers.ModelSerializer):
    """Serializes Cuisine"""

    class Meta:
        model = models.Cuisine
        fields = ("id", "popular_ingredients", "name", "origin")


class DishSerializer(serializers.ModelSerializer):
    """Serializes Dish"""

    class Meta:
        model = models.Dish
        fields = ("id", "ingredients", "name", "price", "serves", "cuisine")


class RestaurantSerializer(serializers.ModelSerializer):
    """Serializes Restaurant"""

    class Meta:
        model = models.Restaurant
        fields = (
            "id",
            "name",
            "owner",
            "established",
            "location",
            "email",
            "contact_number",
            "website",
        )


class MenuSerializer(serializers.ModelSerializer):
    """Serializes Menu"""

    class Meta:
        model = models.Menu
        fields = ("id", "dishes", "cuisines", "restaurant")
