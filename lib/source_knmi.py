#!/usr/bin/env python
# encoding=utf-8

import datetime
import sys
from pyquery import PyQuery
from source import Source

class KNMISource(Source):
  """Weather source class"""

  __baseUrl = 'http://www.knmi.nl/klimatologie/daggegevens/index.cgi?station=370'
  __d = None
  __date = None
  __url = None


  def __init__(self):
    """Constructor"""


  def get_weather(self, day):
    if day >= 0:
      sys.stderr.write('`day` must be an integer and less than 0')
      return None

    date = datetime.datetime.now() + datetime.timedelta(days=day)
    url = self.__get_url(date)

    self.__date = date
    self.__url = url

    self.__d = PyQuery(url=url)

    return self.__parse()


  def __parse(self):
    """Parse the HTML page"""
    rows = self.__d('#printable > table > tr')
    
    w = {}

    w['url'] = self.__url
    w['date'] = self.__date.strftime("%Y-%m-%d")
    w['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    w['temperature_average'] = float(rows.eq(2).find('td').eq(1).text())
    w['temperature_maximum'] = float(rows.eq(3).find('td').eq(1).text())
    w['temperature_minimum'] = float(rows.eq(4).find('td').eq(1).text())

    w['rain_amount'] = float(rows.eq(2).find('td').eq(6).text().lstrip('<'))
    w['rain_duration'] = float(rows.eq(3).find('td').eq(6).text())

    w['sunshine_duration'] = float(rows.eq(7).find('td').eq(1).text())
    w['sunshine_relative'] = int(rows.eq(8).find('td').eq(1).text())

    w['sky_coverage'] = int(rows.eq(9).find('td').eq(1).text())
    w['sky_visibiliy'] = float(rows.eq(11).find('td').eq(1).text())

    w['wind_speed_average'] = float(rows.eq(7).find('td').eq(6).text())
    w['wind_speed_maximum_average'] = float(rows.eq(8).find('td').eq(6).text())
    w['wind_speed_maximum'] = float(rows.eq(9).find('td').eq(6).text())
    w['wind_direction'] = int(rows.eq(11).find('td').eq(6).text())

    w['atmosphere_humidity'] = int(rows.eq(14).find('td').eq(1).text())
    w['atmosphere_pressure'] = float(rows.eq(14).find('td').eq(6).text())


    return w


  def __get_url(self, date):
    """Get the remote URL for fetching the weather"""

    params = {
      'year': date.year,
      'month': date.month,
      'day': date.day
    }

    url = self.__baseUrl
    for key, value in params.iteritems():
      url += '&' + key + '=' + str(value)

    return url
