#!/usr/bin/env python
# encoding=utf-8

import ast
import datetime
import sys
from pyquery import PyQuery
from source import Source

class YrSource(Source):
  """Weather source class"""

  __url = 'http://www.yr.no/place/Netherlands/North_Brabant/Eindhoven/long.html'
  __date = None
  __day = None


  def __init__(self):
    """Constructor"""


  def get_weather(self, day):
    if day < 1 or day > 9:
      sys.stderr.write('`day` must be an integer between 1 and 9')
      return None

    self.__date = datetime.datetime.now() + datetime.timedelta(days=day)
    self.__day = day

    d = PyQuery(url=self.__url)
    return self.__parse(d)


  def __parse(self, d):
    """Parse the HTML page"""
    rows = d('table.yr-table-longterm-detailed > tr')
    
    r = 4 * (self.__day - 1)

    w = {}

    w['metadata'] = {}
    w['metadata']['url'] = self.__url
    w['metadata']['date'] = self.__date.strftime("%Y-%m-%d")
    w['metadata']['today'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    w['temperature'] = {}
    w['temperature']['average'] = []
    for ri in range(4):
      val = rows.eq(r + ri).find('td').eq(2).text()
      val = val.encode('ascii','ignore') # strip the °-sign
      w['temperature']['average'].append(int(val))

    w['rain'] = {}
    w['rain']['amount'] = []
    for ri in range(4):
      val = rows.eq(r + ri).find('td').eq(3).text()
      val = val.rstrip('m') # strip the 'mm'
      w['rain']['amount'].append(float(val))

    w['visual'] = []
    for ri in range(4):
      val = rows.eq(r + ri).find('td').eq(1).find('img').attr('src')
      w['visual'].append(val)

    return w
