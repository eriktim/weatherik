#!/usr/bin/env python
# encoding=utf-8

import ast
import datetime
import re
import sys
import traceback
from pyquery import PyQuery
from source import Source

class YrSource(Source):
  """Weather source class"""

  __d = None
  __date = None
  __day = None
  __url = 'http://www.yr.no/place/Netherlands/North_Brabant/Eindhoven/long.html'


  def __init__(self):
    """Constructor"""


  def get_weather(self, day):
    if day < 1 or day > 9:
      sys.stderr.write('`day` must be an integer between 1 and 9\n')
      return None

    self.__date = datetime.datetime.now() + datetime.timedelta(days=day)
    self.__day = day

    if not self.__d:
      self.__d = PyQuery(url=self.__url)

    data = None
    try:
      data = self.__parse()
    except:
      html = self.__d.outerHtml().encode('ascii', 'replace')
      sys.stderr.write(html)
      sys.stderr.write('\n\n')
      traceback.print_exc()
    return data


  def __parse(self):
    """Parse the HTML page"""
    rows = self.__d('table.yr-table-longterm-detailed > tr')
    
    r = 4 * (self.__day - 1)

    w = {}

    w['url'] = self.__url
    w['date'] = self.__date.strftime("%Y-%m-%d")
    w['url_timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    w['day'] = self.__day

    for ri in range(4):
      val = rows.eq(r + ri).find('td').eq(1).find('img').attr('src')
      w['icon_' + str(ri + 1)] = val

    for ri in range(4):
      val = rows.eq(r + ri).find('td').eq(2).text()
      val = val.encode('ascii','ignore') # strip the °-sign
      w['temperature_average_' + str(ri + 1)] = int(val)

    for ri in range(4):
      val = rows.eq(r + ri).find('td').eq(3).text()
      val = val.rstrip('m') # strip the 'mm'
      w['rain_amount_' + str(ri + 1)] = float(val)

    for ri in range(4):
      val = rows.eq(r + ri).find('td').eq(4).attr('title')
      match = re.search('([0-9]+) m/s from ([a-z]+)', val)
      w['wind_speed_' + str(ri + 1)] = match.group(1)
      w['wind_direction_' + str(ri + 1)] = match.group(2)

    return w
