from rest_framework import viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core import serializers, models, permissions


class IngredientsViewSet(viewsets.ModelViewSet):
    """Ingredients ViewSet"""

    serializer_class = serializers.IngredientSerializer
    queryset = models.Ingredient.objects.all()
    permission_classes = (
        IsAuthenticated,
        permissions.UpdateInformation,
    )
    authentication_classes = (TokenAuthentication,)
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = "__all__"
    ordering_fields = "__all__"


class CuisinesViewSet(viewsets.ModelViewSet):
    """Cuisines ViewSet"""

    serializer_class = serializers.CuisineSerializer
    queryset = models.Cuisine.objects.all()
    permission_classes = (
        IsAuthenticated,
        permissions.UpdateInformation,
    )
    authentication_classes = (TokenAuthentication,)
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = "__all__"
    ordering_fields = "__all__"


class DishesViewSet(viewsets.ModelViewSet):
    """Dishes ViewSet"""

    serializer_class = serializers.DishSerializer
    queryset = models.Dish.objects.all()
    permission_classes = (
        IsAuthenticated,
        permissions.UpdateInformation,
    )
    authentication_classes = (TokenAuthentication,)
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = "__all__"
    ordering_fields = "__all__"


class RestaurantViewSet(viewsets.ModelViewSet):
    """Restaurant ViewSet"""

    serializer_class = serializers.RestaurantSerializer
    queryset = models.Restaurant.objects.all()
    permission_classes = (
        IsAuthenticated,
        permissions.UpdateInformation,
    )
    authentication_classes = (TokenAuthentication,)
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = "__all__"
    ordering_fields = "__all__"


class MenuViewSet(viewsets.ModelViewSet):
    """Menu ViewSet"""

    serializer_class = serializers.MenuSerializer
    queryset = models.Menu.objects.all()
    permission_classes = (
        IsAuthenticated,
        permissions.UpdateInformation,
    )
    authentication_classes = (TokenAuthentication,)
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = "__all__"
    ordering_fields = "__all__"
