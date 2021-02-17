from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Handles creating and updating user"""

    def create_user(self, email, password=None, **extra_fields):
        """Create a new user given an email and password"""
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields,)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """Create and save a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user Model for a user with email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Ingredient(models.Model):
    """Stores ingredient name and price"""

    name = models.CharField(max_length=255)
    price = models.FloatField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__


class Cuisine(models.Model):
    """Stores cuisine name, popular ingredients, place of origin"""

    popular_ingredients = models.ManyToManyField(Ingredient)
    name = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__


class Dish(models.Model):
    """Stores dish name, ingredients used, price, people served and cuisine"""

    ingredients = models.ManyToManyField(Ingredient)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    serves = models.IntegerField(default=1)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, null=True,)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__

    class Meta:
        verbose_name_plural = "Dishes"


class Restaurant(models.Model):
    """Stores information of restaurant"""

    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    established = models.DateField(default=timezone.now)
    location = models.CharField(max_length=255)
    email = models.EmailField()
    contact_number = models.CharField(max_length=255)
    website = models.URLField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__


class Menu(models.Model):
    """Stores the dishes, cuisines"""

    dishes = models.ManyToManyField(Dish)
    cuisines = models.ManyToManyField(Cuisine, blank=True)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, null=True,
    )

    def __str__(self):
        return self.restaurant

    def __repr__(self):
        return self.__str__
