from django.test import TestCase, client
#from django.urls import reverse
from _datetime import datetime, timedelta
from .serializers import *
from .tasks import PullClimateTask
import requests

class MyCase(TestCase):
    def test_time(self):
        data = {
            'date' : '2017-7-4',
            'time' : '17:00',
            'temp_net' : 28.1,
            'cityId': 1
        }
        ser = ClimateNetSerializer(data=data)
        if ser.is_valid():
            ser.save()
            print(ser.data)
        else:
            print(ser.errors)

    def test_climate(self):
        terminal = Terminal.objects.get(pk='b944a96581ea498e995b8e2e5a9d0e81')
        #climatenet = ClimateNet.objects.get(pk='8508b90558684689bff905f765f923cb')
        serializers = TerminalSerializer(terminal)
        print(serializers['deviceAddr'])

    def test_hour(self):
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        time = now.strftime('%H:00')

        time = '11:31'
        time = datetime.strptime(time,'%H:%M')
        time = time.strftime('%H:00')
        print(type(time))
        print(time)

        # time1 = now.time()
        # time1 = str(timedelta(hours=now.hour+1))[:-3]
        # print(time1)

    def test_task(self):
        city = City.objects.get(pk=1)
        data = {
            'date': '2017-7-4',
            'time': '14:00',
            'temp_net': 34,
            'cityId': city.cityId
        }

        serializer = ClimateNetSerializer(data=data)
        if serializer.is_valid():
            # serializer.save()
            # print(serializer.data)
            data['cityId'] = city
            obj, created = ClimateNet.objects.update_or_create(date=data['date'], time=data['time'], cityId=city,defaults=data)
            #obj, created = ClimateNet.objects.update_or_create(date='2017-7-4',time='14:00',cityId=city.cityId, defaults=data)
            print(str(obj))

        print(serializer.errors)

    def test_task1(self):
        PullClimateTask.save_now_climate()