# -*- coding:utf8 -*-
from .serializers import *
import requests
import json
from datetime import datetime, timedelta
from django_cron import CronJobBase, Schedule
from .my_global import url_climate
# django crontab task
# def my_cron_job():
#     PullClimateTask.save_now_climate()


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 60
    RETRY_AFTER_FAILURE_MINS = 5
    MIN_NUM_FAILURES = 3
    RUN_AT_TIMES = ['00:00','01:00','02:00','03:00','04:00','05:00',
                    '06:00','07:00','08:00','09:00','10:00','11:00',
                    '12:00','13:00','14:00','15:00','16:00','17:00',
                    '18:00','19:00','20:00','21:00','22:00','23:00',]

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, run_at_times=RUN_AT_TIMES,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'climateApp.MyCronJob'

    def do(self):
        PullClimateTask.save_now_climate()



class PullClimateTask(object):

    @staticmethod
    def save_now_climate():
        cities = PullClimateTask.get_all_cities()
        for city in cities:
            status = PullClimateTask.get_now_climate(city)
            if status is not 'Saved':
                print(status)
                return False
            print(status)
        return status

    @staticmethod
    def get_all_cities():
        cities = City.objects.all()
        city = [item for item in cities]
        return city

    @staticmethod
    def get_now_climate(city):
        url_now = url_climate.format('now', city.cityName)
            #'https://free-api.heweather.com/v5/now?city='+city.cityName+'&key=4aa1781d7fe04a998a6cd06c6cdb8467'
        data = requests.get(url_now).text
        data = json.loads(data)
        print(data)
        item = json.loads(json.dumps(data['HeWeather5'])[1:-1])
        status = item.get('status')
        if status != 'ok':
            return status

        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        time = now.strftime('%H:00')

        data = {
            'date': date,
            'time': time,
            'temp_net': item.get('now').get('tmp'),
            'cityId': city.cityId
        }

        serializer = ClimateNetSerializer(data=data)
        #serializer1 = ClimateNetSerializer(data=data1)
        try:
            if serializer.is_valid():
                pass
            data['cityId'] = city
            obj, created = ClimateNet.objects.update_or_create(date=data['date'], time=data['time'], cityId=city, defaults=data)
            print(ClimateNetSerializer(obj).data)

            data['time'] = str(timedelta(hours=now.hour+1))[:-3] if time[:2] != '23' else data['time']
            obj1, created = ClimateNet.objects.update_or_create(date=data['date'], time=data['time'], cityId=city, defaults=data)
            print(ClimateNetSerializer(obj1).data)

        except :
            return "save climate net Error!"
           # return IOError.errno
        return 'Saved'

    @staticmethod
    def get_hourly_climate(city):
        url_hourly = url_climate.format('hourly', city.cityName)
            #'https://free-api.heweather.com/v5/hourly?city=' + city + '&key=4aa1781d7fe04a998a6cd06c6cdb8467'
        data = requests.get(url_hourly).text
        data = json.loads(data)
        print(type(data))
        print(data)

        item = json.loads(json.dumps(data['HeWeather5'])[1:-1])
        # print(item)
        #
        # print(type(item))

        itemhourly = item.get('hourly_forecast')
        print(type(itemhourly))
        print(itemhourly)

        for i in itemhourly:
            print(i.get('date') + "=====" + i.get('tmp'))