#!/usr/bin/env python
# encoding=utf-8

import ast
import datetime
import sys
from pyquery import PyQuery
from source import Source

class WeeronlineSource(Source):
  """Weather source class"""

  __d = None
  __date = None
  __day = None
  __url = 'http://www.weeronline.nl/Europa/Nederland/Eindhoven/4058591'


  def __init__(self):
    """Constructor"""


  def get_weather(self, day):
    if day < 0 or day > 13:
      sys.stderr.write('`day` must be an integer between 0 and 13')
      return None
    if day > 3:
      sys.stderr.write('`day` >= 4 not yet supported')
      return None

    self.__date = datetime.datetime.now() + datetime.timedelta(days=day)
    self.__day = day

    if not self.__d:
      self.__d = PyQuery(url=self.__url)

    return self.__parse()


  def __parse(self):
    """Parse the HTML page"""
    container = self.__d('.weatherforecast.FiveDays')
    rows = container.find('.row_forecast')
    iconRows = container.find('.row_weathericons')
    ratingRows = container.find('.row_weathernumbers')
    
    index = self.__day + 1

    w = {}

    w['url'] = self.__url
    w['date'] = self.__date.strftime("%Y-%m-%d")
    w['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    icons = iconRows.eq(0).find('td').eq(index).find('div')
    for i in range(3):
      val = icons.eq(i).attr('class')
      w['icon_' + str(i + 1)] = val

    val = rows.eq(0).find('td').eq(index).text()
    val = val.encode('ascii', 'ignore') # strip the °-sign
    w['temperature_minimum'] = int(val)

    val = rows.eq(1).find('td').eq(index).text()
    val = val.encode('ascii', 'ignore') # strip the °-sign
    w['temperature_maximum'] = int(val)

    val = rows.eq(2).find('td').eq(index).text()
    val = val.rstrip('/') # strip the '/'
    w['wind_force'] = int(val)

    val = rows.eq(2).find('td').eq(index).find('.windImageDiv.darkImage > div').attr('class')
    val = val.replace('wind_icon_small_', '').replace('_xs darkImage', '')
    w['wind_direction'] = val

    val = rows.eq(3).find('td').eq(index).text()
    val = val.rstrip('%') # strip the '%'
    w['rain_percentage'] = int(val)

    val = rows.eq(4).find('td').eq(index).text()
    val = val.rstrip('m') # strip the 'mm'
    w['rain_amount'] = float(val)

    val = ratingRows.eq(0).find('td').eq(index).text()
    w['rating'] = int(val)

    return w
