from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import *
from rest_framework_simplejwt.authentication import JWTAuthentication
class AMTUserManager(UserManager):
    from django.utils.translation import gettext_lazy as _
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def authenticate(self, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get('username')

        user = self.get_by_natural_key(email)
        if user is not None and user.check_password(password):
            return user

        return None
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser Must have is_staff=True Right?")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Super must have is_superuser privilages!")
        
        return self._create_user(email, password, **extra_fields)
    
    
class User(AbstractUser): 
    from django.utils.translation import gettext_lazy as _
    username = None
    email = models.EmailField(
        _("Email Address"),
        unique=True,
    )
    objects = AMTUserManager()
    full_name = models.CharField(max_length=40)
    is_manager = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    has_valid_passport = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.full_name
    
    
class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="driver_profile")
    is_available = models.BooleanField(default=True)
    
class Destination(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Bus(models.Model):
    name = models.CharField(max_length=100)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    seats = models.PositiveSmallIntegerField(default=0)
    destination = models.ForeignKey(Destination, on_delete=models.PROTECT, related_name="destination")

    def __str__(self):
        return self.name

class Trip(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="trips")
    is_daily = models.BooleanField(default=False)
    estimated_trip_time = models.PositiveSmallIntegerField()
    is_full = models.BooleanField(default=False)
    date = models.DateTimeField()
    passengers = models.PositiveSmallIntegerField(default=0)
    
    
    
class Ticket(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="tickets")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    date = models.DateTimeField(auto_now_add=True)

    
    