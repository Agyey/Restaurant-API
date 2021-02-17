from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register("ingredients", views.IngredientsViewSet, basename="ingredient")
router.register("dishes", views.DishesViewSet, basename="dish")
router.register("restaurant", views.RestaurantViewSet, basename="restaurant")
router.register("menu", views.MenuViewSet, basename="menu")
router.register("cuisines", views.CuisinesViewSet, basename="cuisine")


urlpatterns = [
    path("", include(router.urls)),
]
