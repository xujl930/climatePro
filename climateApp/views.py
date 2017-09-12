from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import *
from datetime import datetime
from .tasks import PullClimateTask
from django.conf import settings
from django.contrib.auth.models import User
from django.db import connection, transaction
import json


# @api_view(['POST'])
# def token(request):
#     if request.method == 'POST':
#         try:
#             token = Token.objects.get(user=request.user)
#         except Token.DoesNotExist:
#             return Response({r'no found user token':request.user.username}, status=status.HTTP_404_NOT_FOUND)
#
#         return Response(token, status=status.HTTP_200_OK)

@api_view(['POST'])
def save_climate(request):
    if request.method == 'POST':
        stat = PullClimateTask.save_now_climate()
        return Response(stat)


@api_view(['GET', 'POST'])
def post_city(request):
    if request.method == 'GET':
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = {
            'cityName': request.data.get('cityName')
        }
        serializer = CitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_post_terminal(request):
    # get all terminal
    if request.method == 'GET':
        terminals = Terminal.objects.all()

        flag = False
        qd = request.GET
        qd_len = len(qd.dict())

        if qd_len == 1:
            if 'deviceEui' in qd:
                deveui = qd.get('deviceEui', None)
                if deveui is not None:
                    terminals = terminals.filter(deviceEui=deveui)
                    flag = True
            elif 'deviceAddr' in qd:
                devaddr = qd.get('deviceAddr', None)
                if devaddr is not None:
                    terminals = terminals.filter(deviceAddr=devaddr)
                    flag = True
            else:
                return Response({'error in param': qd.dict()}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TerminalSerializer(terminals, many=True)

        if not terminals.count() and flag is True:
            return Response(terminals.all(), status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.data)

    if request.method == 'POST':
        data = {
            'deviceEui': str(request.data.get('deviceEui')).strip(),
            'deviceAddr': request.data.get('deviceAddr'),
            'userId': request.data.get('userId')
        }
        serializer = TerminalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH'])
def get_patch_single_terminal(request, pk):
    try:
        terminal = Terminal.objects.get(pk=pk)
    except Terminal.DoesNotExist:
        return Response({'no such terminal': pk}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TerminalSerializer(terminal)
        return Response(serializer.data)

    if request.method == 'PATCH':
        if len(request.data) > 1:
            return Response('too many fields given!', status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('deviceAddr', None) is None:
            return Response('Not deviceAddr field!', status=status.HTTP_400_BAD_REQUEST)

        serializer = TerminalSerializer(terminal, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_post_climate(request, pk):
    try:
        terminal = Terminal.objects.get(pk=pk)
    except Terminal.DoesNotExist:
        return Response({'no such terminal': pk}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        cityid = terminal.deviceAddr.get_cityid()
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        hour = now.strftime('%H')

        climates = ClimateNet.objects.filter(cityId=cityid, date=date, time__hour=hour)
        if len(climates) == 0:
            return Response({'got no temper in': now.strftime('%Y-%m-%d %H:%M')}, status=status.HTTP_404_NOT_FOUND)
        if len(climates) > 1:
            return Response({'got many temper in': now.strftime('%Y-%m-%d %H:%M')}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClimateNetSerializer(climates[0])
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        time = request.data.get('time')
        try:
            time = datetime.strptime(time, '%H:%M:%S')
        except ValueError:
            return Response({'error time format': time}, status=status.HTTP_400_BAD_REQUEST)
        time = time.strftime('%H:00')
        data = {
            'date': request.data.get('date'),
            'time': time,
            'temp_inner': request.data.get('temp_inner'),
            'terminalId': str(pk).replace('-', '')
        }
        serializer = ClimateInnerSerializer(data=data)
        if serializer.is_valid():
            pass
        data['terminalId'] = terminal
        obj, created = ClimateInner.objects.update_or_create(date=data['date'], time=data['time'],
                                                             terminalId=terminal, defaults=data)
        print(ClimateInnerSerializer(obj).data)
        # serializer.save()
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(ClimateInnerSerializer(obj).data, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_hours_climate(request, pk1, pk2):
    try:
        terminal = Terminal.objects.get(pk=pk1)
    except Terminal.DoesNotExist:
        return Response({'no such terminal': pk1}, status=status.HTTP_404_NOT_FOUND)

    cityid = terminal.deviceAddr.get_cityid()
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')
    hour = now.strftime('%H')

    pk2 = abs(int(pk2))
    time = int(hour) + pk2

    if time > 23:
        time = 23

    if int(pk2) == 0:
        climates = ClimateNet.objects.get(cityId=cityid, date=date, time__hour=hour)
        serializer = ClimateNetSerializer(climates)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        climates = ClimateNet.objects.filter(cityId=cityid, date=date,
                                             time__hour__range=(int(hour) + 1, time)).order_by('time')
        if len(climates) == 0:
            return Response({'got no temper in': now.strftime('%Y-%m-%d %H:00')}, status=status.HTTP_404_NOT_FOUND)
        serializer = ClimateNetSerializer(climates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_day_climate(request, pk1, pk2):
    try:
        terminal = Terminal.objects.get(pk=pk1)
    except Terminal.DoesNotExist:
        return Response({'no such terminal': pk1}, status=status.HTTP_404_NOT_FOUND)

    try:
        date = datetime.strptime(str(pk2), '%Y-%m-%d')
    except ValueError:
        return Response({"bad date format": pk2}, status=status.HTTP_400_BAD_REQUEST)

    cityid = terminal.deviceAddr.get_cityid()

    sql1 = r"SELECT DISTINCT n.date, n.time, n.temp_net, i.temp_inner " \
           r"FROM climate_net n LEFT JOIN  climate_inner i " \
           r"ON n.date=i.date AND n.time=i.time AND i.terminalId = %s " \
           r"WHERE n.cityId = %s AND n.date = %s " \
           r"UNION "

    sql2 = r"SELECT DISTINCT i.date, i.time, n.temp_net, i.temp_inner " \
           r"FROM climate_net n RIGHT JOIN climate_inner i " \
           r"ON n.date=i.date AND n.time=i.time AND n.cityId = %s " \
           r"WHERE i.terminalId = %s AND i.date = %s " \
           r"ORDER BY TIME"

    sql = sql1 + sql2
    climates = DayClimate.get_climates(sql, [pk1, cityid, pk2, cityid, pk1, pk2])
    return Response(climates, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_week_climate(request, pk, begin, end):
    try:
        terminal = Terminal.objects.get(pk=pk)
    except Terminal.DoesNotExist:
        return Response({'no such terminal': pk}, status=status.HTTP_404_NOT_FOUND)

    try:
        datetime.strptime(str(begin), '%Y-%m-%d')
        datetime.strptime(str(end), '%Y-%m-%d')
    except ValueError:
        return Response({"bad date format":""}, status=status.HTTP_400_BAD_REQUEST)
    cityid = terminal.deviceAddr.get_cityid()

    sql = r"SELECT DISTINCT n.date, truncate(avg(n.temp_net), 2) as 'avg_net', truncate(avg(i.temp_inner), 2) as 'avg_inner' " \
          r"FROM climate_net n LEFT JOIN climate_inner i " \
          r"ON n.date = i.date AND i.terminalId = %s " \
          r"WHERE n.date between %s and %s AND n.cityId = %s group by date"

    climates = WeekClimate.get_climates(sql, [pk, begin, end, cityid])
    return Response(climates, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def get_post_user(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = {
            'userId': request.data.get('userId'),
            'password': request.data.get('password'),
            'displayName': request.data.get('displayName'),
            'email': request.data.get('email'),
            'mobile': request.data.get('mobile'),
            'role': request.data.get('role')
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH'])
def get_patch_single_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    if request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
