#!/usr/bin/env python
# encoding=utf-8

from source_knmi import KNMISource
from source_weeronline import WeeronlineSource
from source_yr import YrSource

knmi = KNMISource()
print knmi.get_weather_yesterday()

weeronline = WeeronlineSource()
print weeronline.get_weather_tomorrow()

yr = YrSource()
print yr.get_weather_tomorrow()
