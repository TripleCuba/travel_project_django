import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from cloudinary.models import CloudinaryField


class Destination(models.Model):
    destination = models.CharField(max_length=150)
    description = models.CharField(max_length=400)
    image = CloudinaryField('image')
    @property
    def get_img(self):
        return (
            f'https://res.cloudinary.com/dkeewhdlg/destiantions/{self.image}'
        )


    def __str__(self):
        return self.destination


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('User must have an email!')
        if not username:
            raise ValueError('User must have an username!')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):

    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class Profile(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='profile')
    firstName = models.CharField(max_length=100, blank=True, null=True)
    lastName = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    town = models.CharField(max_length=100, blank=True, null=True)
    image = CloudinaryField('profileImage')

    @property
    def get_img(self):
        return (
            f'https://res.cloudinary.com/dkeewhdlg/{self.image}'
        )

    def __str__(self):
        return f'Account{self.account} first name {self.firstName}'

class Town(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=400)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    image = CloudinaryField('image')

    @property
    def get_img(self):
        return (
            f'https://res.cloudinary.com/dkeewhdlg/{self.image}'
        )

    def __str__(self):
        return self.title


class Hotel(models.Model):
    title = models.CharField(max_length=120)
    rating = models.FloatField(null=True, blank=True)
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    image = CloudinaryField('hotel', )

    @property
    def get_img(self):
        return {f'https://res.cloudinary.com/dkeewhdlg/{self.image}'}

    def __str__(self):
        return self.title


class Room(models.Model):
    title = models.CharField(max_length=100)
    room_number = models.CharField(max_length=50)
    capacity = models.IntegerField()
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    price_per_guest = models.FloatField()
    is_available = models.BooleanField(default=True)
    image = CloudinaryField('image')

    @property
    def get_img(self):
        return {f'https://res.cloudinary.com/dkeewhdlg/{self.image}'}

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    total_price = models.FloatField()
    date_ordered = models.DateTimeField(default=datetime.datetime.now())
    guests = models.IntegerField()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
