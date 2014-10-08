var fs = require('fs');
var request = require('request');
var cheerio = require('cheerio');

url = 'http://www.weeronline.nl/Europa/Nederland/Eindhoven/4058591';

request(url, function(err, response, html) {

  if (err) {
    console.error('Failed fetching url');
    system.exit(1);
  }

  /**
   * @type {number} day
   */
  function get_weather_object(day) {
    if (day < 0 || day > 4) {
      return null;
    }
    var index = day + 1;
    var json = {};
    $('.weatherforecast.FiveDays').filter(function() {
      forecastRows = $(this).find('.row_forecast');
      json.min = parseInt(forecastRows.eq(0).find('td').eq(index).text());
      json.max = parseInt(forecastRows.eq(1).find('td').eq(index).text());
      json.bft = parseInt(forecastRows.eq(2).find('td').eq(index).text());
      json.pct = parseInt(forecastRows.eq(3).find('td').eq(index).text());
      json.mm  = parseInt(forecastRows.eq(4).find('td').eq(index).text());

      weatherIconsRows = $(this).find('.row_weathericons');
      var divs = weatherIconsRows.eq(0).find('td').eq(index).find('div');
      // TODO decode
      json.icons = [
        divs.eq(0).attr('class'),
        divs.eq(1).attr('class'),
        divs.eq(2).attr('class')
      ];
    });
    return json;
  }

  var $ = cheerio.load(html);
  console.log(JSON.stringify(get_weather_object(1), null, '  '));
  console.log(JSON.stringify(get_weather_object(3), null, '  '));
});
