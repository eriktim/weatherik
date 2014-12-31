#!/usr/bin/env python
# encoding=utf-8

from db import Database
from source_knmi import KNMISource
from source_weeronline import WeeronlineSource
from source_yr import YrSource

db = Database()

knmi = KNMISource()
data = knmi.get_weather_yesterday()
db.insert('source_knmi', data)

weeronline = WeeronlineSource()
data = weeronline.get_weather_tomorrow()
db.insert('source_weeronline', data)
data = weeronline.get_weather_three_days()
db.insert('source_weeronline', data)

yr = YrSource()
data = yr.get_weather_tomorrow()
db.insert('source_yr', data)
data = yr.get_weather_three_days()
db.insert('source_yr', data)
