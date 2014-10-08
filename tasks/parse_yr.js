var fs = require('fs');
var request = require('request');
var cheerio = require('cheerio');

url = 'http://www.yr.no/place/Netherlands/North_Brabant/Eindhoven/long.html';

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
    var index = 4 * (day - 1) - 1;
    var json = {};
    rows = $('table.yr-table-longterm-detailed > tr');
    var t1 = parseInt(rows.eq(index + 1).find('td').eq(2).text());
    var t2 = parseInt(rows.eq(index + 2).find('td').eq(2).text());
    var t3 = parseInt(rows.eq(index + 3).find('td').eq(2).text());
    var t4 = parseInt(rows.eq(index + 4).find('td').eq(2).text());
    json.min = Math.min(t1, t2, t3, t4);
    json.max = Math.max(t1, t2, t3, t4);

    var mm1 = parseFloat(rows.eq(index + 1).find('td').eq(3).text());
    var mm2 = parseFloat(rows.eq(index + 2).find('td').eq(3).text());
    var mm3 = parseFloat(rows.eq(index + 3).find('td').eq(3).text());
    var mm4 = parseFloat(rows.eq(index + 4).find('td').eq(3).text());
    json.mm = mm1 + mm2 + mm3 + mm4;

    return json;
  }

  var $ = cheerio.load(html);
  console.log(JSON.stringify(get_weather_object(1), null, '  '));
  console.log(JSON.stringify(get_weather_object(3), null, '  '));
});
