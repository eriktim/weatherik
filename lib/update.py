#!/usr/bin/env python
# encoding=utf-8

import sys
from db import Database
from source_knmi import KNMISource
from source_weeronline import WeeronlineSource
from source_yr import YrSource

db = Database()
error = False

knmi = KNMISource()
data = knmi.get_weather_yesterday()
if data:
  db.insert('source_knmi', data)
else:
  error = True

weeronline = WeeronlineSource()
data = weeronline.get_weather_tomorrow()
if data:
  db.insert('source_weeronline', data)
else:
  error = True
data = weeronline.get_weather_three_days()
if data:
  db.insert('source_weeronline', data)
else:
  error = True

yr = YrSource()
data = yr.get_weather_tomorrow()
if data:
  db.insert('source_yr', data)
else:
  error = True
data = yr.get_weather_three_days()
if data:
  db.insert('source_yr', data)
else:
  error = True

if error:
  sys.stderr.write('Not all sources were parsed successfully\n')
  sys.exit(1)
