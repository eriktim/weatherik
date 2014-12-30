#!/usr/bin/env python
# encoding=utf-8

import abc

class Source(object):
  """Weather source class"""
  __metaclass__  = abc.ABCMeta

  def __init__(self):
    """Constructor"""

  @abc.abstractmethod
  def get_weather(self, day):
    """Get the weather forecast for `day` days from now"""

  def get_weather_yesterday(self):
    """Get the weather from yesterday"""
    return self.get_weather(-1)

  def get_weather_tomorrow(self):
    """Get tomorrow's weather forecast"""
    return self.get_weather(1)

  def get_weather_three_days(self):
    """Get the 3-days-ahead weather forecast"""
    return self.get_weather(3)

  def get_weather_next_week(self):
    """Get the weather forecast for next week"""
    return self.get_weather(7)
