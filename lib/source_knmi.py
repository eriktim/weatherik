#!/usr/bin/env python
# encoding=utf-8

import datetime
import sys
from pyquery import PyQuery
from source import Source

class KNMISource(Source):
  """Weather source class"""

  __baseUrl = 'http://www.knmi.nl/klimatologie/daggegevens/index.cgi?station=370'
  __url = None
  __date = None


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

    d = PyQuery(url=url)
    return self.__parse(d)


  def __parse(self, d):
    """Parse the HTML page"""
    rows = d('#printable > table > tr')
    
    w = {}

    w['metadata'] = {}
    w['metadata']['url'] = self.__url
    w['metadata']['date'] = self.__date.strftime("%Y-%m-%d")
    w['metadata']['today'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    w['temperature'] = {}
    w['temperature']['average'] = float(rows.eq(2).find('td').eq(1).text())
    w['temperature']['maximum'] = float(rows.eq(3).find('td').eq(1).text())
    w['temperature']['minimum'] = float(rows.eq(4).find('td').eq(1).text())

    w['rain'] = {}
    w['rain']['amount'] = float(rows.eq(2).find('td').eq(6).text().lstrip('<'))
    w['rain']['duration'] = float(rows.eq(3).find('td').eq(6).text())

    w['sky'] = {}
    w['sky']['sunshine'] = {}
    w['sky']['sunshine']['duration'] = float(rows.eq(7).find('td').eq(1).text())
    w['sky']['sunshine']['relative'] = int(rows.eq(8).find('td').eq(1).text())
    w['sky']['coverage'] = int(rows.eq(9).find('td').eq(1).text())
    w['sky']['visibiliy'] = float(rows.eq(11).find('td').eq(1).text())

    w['wind'] = {}
    w['wind']['average'] = float(rows.eq(7).find('td').eq(6).text())
    w['wind']['maximum'] = {}
    w['wind']['maximum']['average'] = float(rows.eq(8).find('td').eq(6).text())
    w['wind']['maximum']['absolute'] = float(rows.eq(9).find('td').eq(6).text())
    w['wind']['direction'] = int(rows.eq(11).find('td').eq(6).text())

    w['atmosphere'] = {}
    w['atmosphere']['humidity'] = int(rows.eq(14).find('td').eq(1).text())
    w['atmosphere']['pressure'] = float(rows.eq(14).find('td').eq(6).text())


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
