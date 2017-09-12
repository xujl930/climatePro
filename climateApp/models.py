from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import User
import uuid

# User._meta.get_field('email')._unique = True

# 注册signal，确保添加用户，生成token
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        print("user is added")
        Token.objects.create(user=instance)


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, to_field='username', db_column='user',
                                on_delete=models.CASCADE)
    displayName = models.CharField(max_length=45, blank=True, null=True)
    mobile = models.CharField(max_length=11, blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    # userId = models.CharField(primary_key=True, max_length=20)
    # password = models.CharField(max_length=100)
    # email = models.CharField(max_length=40, blank=True, null=True)
    #
    class Meta:
        db_table = 'user_profile'


class City(models.Model):
    """
    City Model
    定义城市的属性
    """
    cityId = models.AutoField(primary_key=True)
    cityName = models.CharField(max_length=20, unique=True, null=False)

    class Meta:
        db_table = 'city'

    def get_cityid(self):
        return self.cityId

    @classmethod
    def get_cityname(cls):
        return cls.cityName


class Terminal(models.Model):
    terminalId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deviceEui = models.CharField(max_length=20, unique=True, db_index=True, null=False)
    deviceAddr = models.ForeignKey('City', to_field='cityName', db_column='deviceAddr', on_delete=models.CASCADE)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='username', db_column='user',
                                 on_delete=models.CASCADE)

    class Meta:
        db_table = 'terminal'


class ClimateNet(models.Model):
    climateNetId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    temp_net = models.FloatField()
    cityId = models.ForeignKey('City', db_column='cityId', on_delete=models.CASCADE)

    class Meta:
        db_table = 'climate_net'
        unique_together = ('date', 'time', 'cityId')


class ClimateInner(models.Model):
    climateId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    temp_inner = models.FloatField()
    terminalId = models.ForeignKey('Terminal', db_column='terminalId', on_delete=models.CASCADE)

    class Meta:
        db_table = 'climate_inner'
        unique_together = ('date', 'time', 'terminalId')
