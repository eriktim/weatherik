#!/usr/bin/env python
# encoding=utf-8

import ast
import datetime
import sys
from pyquery import PyQuery
from source import Source

class WeeronlineSource(Source):
  """Weather source class"""

  __url = 'http://www.weeronline.nl/Europa/Nederland/Eindhoven/4058591'
  __date = None
  __day = None


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

    d = PyQuery(url=self.__url)
    return self.__parse(d)


  def __parse(self, d):
    """Parse the HTML page"""
    container = d('.weatherforecast.FiveDays')
    rows = container.find('.row_forecast')
    iconRows = container.find('.row_weathericons')
    
    index = self.__day + 1

    w = {}

    w['metadata'] = {}
    w['metadata']['url'] = self.__url
    w['metadata']['date'] = self.__date.strftime("%Y-%m-%d")
    w['metadata']['today'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    w['temperature'] = {}
    val = rows.eq(0).find('td').eq(index).text()
    val = val.encode('ascii','ignore') # strip the °-sign
    w['temperature']['minimum'] = int(val)
    val = rows.eq(1).find('td').eq(index).text()
    val = val.encode('ascii','ignore') # strip the °-sign
    w['temperature']['maximum'] = int(val)

    w['rain'] = {}
    val = rows.eq(4).find('td').eq(index).text()
    val = val.rstrip('m') # strip the 'mm'
    w['rain']['amount'] = float(val)

    w['visual'] = []
    icons = iconRows.eq(0).find('td').eq(index).find('div')
    for i in range(3):
      val = icons.eq(i).attr('class')
      w['visual'].append(val)

    return w
