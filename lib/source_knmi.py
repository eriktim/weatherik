#!/usr/bin/env python
# encoding=utf-8

import datetime
import sys
import traceback
from pyquery import PyQuery
from source import Source

class KNMISource(Source):
  """Weather source class"""

  __baseUrl = 'http://www.knmi.nl/klimatologie/daggegevens/index.cgi?station=370'
  __d = None
  __date = None
  __day = None
  __url = None


  def __init__(self):
    """Constructor"""


  def get_weather(self, day):
    if day >= 0:
      sys.stderr.write('`day` must be an integer and less than 0\n')
      return None

    date = datetime.datetime.now() + datetime.timedelta(days=day)
    url = self.__get_url(date)

    self.__date = date
    self.__day = day
    self.__url = url

    self.__d = PyQuery(url=url)

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
    rows = self.__d('#printable > table > tr')
    
    w = {}

    w['url'] = self.__url
    w['date'] = self.__date.strftime("%Y-%m-%d")
    w['url_timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    w['day'] = self.__day

    w['temperature_average'] = self.__numeric(rows.eq(2).find('td').eq(1).text())
    w['temperature_maximum'] = self.__numeric(rows.eq(3).find('td').eq(1).text())
    w['temperature_minimum'] = self.__numeric(rows.eq(4).find('td').eq(1).text())

    w['rain_amount'] = self.__numeric(rows.eq(2).find('td').eq(6).text().lstrip('<-'))
    w['rain_duration'] = self.__numeric(rows.eq(3).find('td').eq(6).text().lstrip('-'))

    w['sunshine_duration'] = self.__numeric(rows.eq(7).find('td').eq(1).text())
    w['sunshine_relative'] = self.__numeric(rows.eq(8).find('td').eq(1).text())

    w['sky_coverage'] = self.__numeric(rows.eq(9).find('td').eq(1).text())
    w['sky_visibiliy'] = self.__numeric(rows.eq(11).find('td').eq(1).text())

    w['wind_speed_average'] = self.__numeric(rows.eq(7).find('td').eq(6).text())
    w['wind_speed_maximum_average'] = self.__numeric(rows.eq(8).find('td').eq(6).text())
    w['wind_speed_maximum'] = self.__numeric(rows.eq(9).find('td').eq(6).text())
    w['wind_direction'] = self.__numeric(rows.eq(11).find('td').eq(6).text())

    w['atmosphere_humidity'] = self.__numeric(rows.eq(14).find('td').eq(1).text())
    w['atmosphere_pressure'] = self.__numeric(rows.eq(14).find('td').eq(6).text())


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


  def __numeric(self, x):
    x = x.rstrip('-')
    if not x:
      return 0
    return float(x) if '.' in x else int(x)
