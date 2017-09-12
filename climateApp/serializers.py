# -*- coding:utf8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import *
from django.db import connection
from django.conf import settings
from django.contrib.auth.models import User


# import json
# import requests
# from datetime import datetime, timedelta


class CitySerializer(serializers.ModelSerializer):
    cityName = serializers.CharField(max_length=20, allow_null=False)

    class Meta:
        model = City
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # userId = serializers.CharField(max_length=20, allow_null=False)
    # password = serializers.CharField(max_length=100, allow_null=False)
    # role = serializers.CharField(max_length=10, allow_null=False)

    class Meta:
        model = User
        fields = '__all__'
        # exclude = ('password',)


class TerminalSerializer(serializers.ModelSerializer):
    terminalId = serializers.PrimaryKeyRelatedField(read_only=True, pk_field=serializers.UUIDField(format='hex'))
    deviceEui = serializers.CharField(max_length=20, allow_null=False,
                                      validators=[UniqueValidator(queryset=Terminal.objects.all())])

    class Meta:
        model = Terminal
        fields = '__all__'

    def get_city(self):
        return self['deviceAddr']

        # def validated_deviceAddr(self,deviceaddr):
        #     data = City.objects.get(cityName=deviceaddr)
        #     if data is None:
        #         raise serializers.ValidationError("city "+deviceaddr+" is not exist")
        #     return data


class ClimateNetSerializer(serializers.ModelSerializer):
    climateNetId = serializers.PrimaryKeyRelatedField(read_only=True, pk_field=serializers.UUIDField(format='hex'))
    date = serializers.DateField(format='%Y-%m-%d', allow_null=False)
    time = serializers.TimeField(format='%H:%M', allow_null=False)

    class Meta:
        model = ClimateNet
        fields = '__all__'


class ClimateInnerSerializer(serializers.ModelSerializer):
    climateId = serializers.PrimaryKeyRelatedField(read_only=True, pk_field=serializers.UUIDField(format='hex'))
    #    terminalId = serializers.PrimaryKeyRelatedField(read_only=True, pk_field=serializers.UUIDField(format='hex'))
    date = serializers.DateField(format='%Y-%m-%d', allow_null=False)
    time = serializers.TimeField(format='%H', allow_null=False)

    terminalId = serializers.PrimaryKeyRelatedField(read_only=True, pk_field=serializers.UUIDField(format='hex'))

    class Meta:
        model = ClimateInner
        fields = '__all__'
        # exclude = ('terminalId',)


class DayClimate(object):
    @staticmethod
    def get_climates(sql, param):
        with connection.cursor() as cursor:
            cursor.execute(sql, param)
            return DayClimate.dictfetchall(cursor)

    @staticmethod
    def dictfetchall(cursor):
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

class WeekClimate(DayClimate):
    pass


# class DayClimateEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o,DayClimate):
#             return eval(o.__repr__())
#         return json.JSONEncoder.default(self,o)

# class PullClimateTask(object):
#
#     @staticmethod
#     def save_now_climate():
#         cities = PullClimateTask.get_all_cities()
#         for city in cities:
#             status = PullClimateTask.get_now_climate(city)
#             if status is not True:
#                 print(status)
#                 return False
#             print(status)
#
#     @staticmethod
#     def get_all_cities():
#         cities = City.objects.all()
#         city = [item for item in cities]
#         return city
#
#     @staticmethod
#     def get_now_climate(city):
#         url_now = 'https://free-api.heweather.com/v5/now?city='+city.cityName+'&key=4aa1781d7fe04a998a6cd06c6cdb8467'
#         data = requests.get(url_now).text
#         data = json.loads(data)
#         print(data)
#         item = json.loads(json.dumps(data['HeWeather5'])[1:-1])
#         status = item.get('status')
#         if status != 'ok':
#             return status
#
#         now = datetime.now()
#         date = now.strftime('%Y-%m-%d')
#         time = now.strftime('%H:00')
#         time1 = str(timedelta(hours=now.hour+1))[:-3]
#
#         data = {
#             'date': date,
#             'time': time,
#             'temp_net': item.get('now').get('tmp'),
#             'cityId': city.cityId
#         }
#         data1 = {
#             'date': date,
#             'time': time1,
#             'temp_net': item.get('now').get('tmp'),
#             'cityId': city.cityId
#         }
#
# serializer = ClimateNetSerializer(data=data) serializer1 = ClimateNetSerializer(data=data1) try: if
# serializer.is_valid(): data['cityId'] = city obj, created = ClimateNet.objects.update_or_create(date=data['date'],
# time=data['time'], cityId=city, defaults=data) print(obj, created) if serializer1.is_valid(): data1['cityId'] =
# city obj1, created = ClimateNet.objects.update_or_create(date=data1['date'], time=data1['time'], cityId=city,
# defaults=data1) print(obj1, created) except IOError: return IOError.errno # print(item.get('now').get('date')) #
# print(item.get('now').get('tmp')) return True
#
#     @staticmethod
#     def get_hourly_climate(city):
#         url_hourly = 'https://free-api.heweather.com/v5/hourly?city=' + city + '&key=4aa1781d7fe04a998a6cd06c6cdb8467'
#         data = requests.get(url_hourly).text
#         data = json.loads(data)
#         print(type(data))
#         print(data)
#
#         item = json.loads(json.dumps(data['HeWeather5'])[1:-1])
#         # print(item)
#         #
#         # print(type(item))
#
#         itemhourly = item.get('hourly_forecast')
#         print(type(itemhourly))
#         print(itemhourly)
#
#         for i in itemhourly:
#             print(i.get('date') + "=====" + i.get('tmp'))
