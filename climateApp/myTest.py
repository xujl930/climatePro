# -*- coding:utf8 -*-
from .models import *
from .serializers import *

def tt():
    terminal = Terminal.objects.get(pk='b944a96581ea498e995b8e2e5a9d0e81')
    #climatenet = ClimateNet.objects.get(pk='8508b90558684689bff905f765f923cb')
    print(terminal.get_city())

