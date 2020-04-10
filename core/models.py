"""Core models"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manages user mapped objects"""

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    #user_id = models.IntegerField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Address(models.Model):
    """ Address model """

    #address_id = models.IntegerField(primary_key=True)
    street = models.CharField(max_length=255)
    outdoor_number = models.CharField(max_length=255)
    indoor_number = models.CharField(max_length=255)
    suburb = models.CharField(max_length=255)
    zip_code = models.IntegerField()
    town = models.CharField(max_length=255)
    state = models.CharField(max_length=255)


class Profile(models.Model):
    """ Profile model """

    #profile_id = models.IntegerField(primary_key=True, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)


class Restaurnat(models.Model):
    """ Restaurant model """

    #restaurnat_id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


class Menu(models.Model):
    """ Menu model """
    #menu_id = models.CharField(primary_key=True)
    restaurant_id = models.ForeignKey(Restaurnat, on_delete=models.CASCADE)


class Item(models.Model):
    """ Item model """

    #item_id = models.CharField(primary_key=True)
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    #image = models.ImageField(upload_to="images")
    description = models.CharField(max_length=255)
    price = models.FloatField()


class ShoppingCart(models.Model):
    """ Shopping cart models """

    #shopping_cart_id = models.IntegerField(primary_key=True, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()


class ItemSet(models.Model):
    """ Item set model """

    #item_set_id = models.IntegerField(primary_key=True)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    shopping_cart_id = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    subtotal = models.FloatField()


class Order(models.Model):
    """ Order model """

    #order_id = models.IntegerField(primary_key=True)
    shoppng_cart_id = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)
    delivery_man = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True, null=True)
    delivered = models.BooleanField(default=False)