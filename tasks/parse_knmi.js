var fs = require('fs');
var request = require('request');
var cheerio = require('cheerio');
var mongo = require('mongojs');

/**
 * @type {number} day
 */
function get_weather_object(day, callback) {
  if (day >= 0) {
    return null;
  }

  var date = new Date();
  date.setDate(date.getDate() + day);

  var params = {
    year: date.getFullYear(),
    month: date.getMonth() + 1,
    day: date.getDate()
  };

  url = 'http://www.knmi.nl/klimatologie/daggegevens/index.cgi?station=370';
  for (key in params) {
    url += '&' + key + '=' + params[key];
  }

  request(url, function(err, response, html) {
    if (err) {
      console.error('Failed fetching url');
      system.exit(1);
    }
    var json = {
      temperature: {
        average: null,
        minimum: null,
        maximum: null
      },
      rain: {
        amount: null, // mm
        duration: null // hours
      },
      sky: {
        sunshine: {
          duration: null, // hours
          relative: null // %
        },
        coverage: null, // octa's
        visibiliy: null // km
      },
      wind: {
        average: null, // m/s
        maximum: {
          average: null, // m/s
          absolute: null // m/s
        },
        direction: null
      },
      atmosphere: {
        humidity: null, // %
        pressure: null // hPa
      },
      metadata: {
        url: null,
        date: null
      }
    };

    // fix syntax error in knmi site
    html = html.replace(/<div align=right>\s*(\d+\.?\d*\s*<\/td>)/g, '$1');
    html = html.replace(/(<th >\s*Gemiddelde luchtdruk)\s*<\/div>/g, '$1');
    var $ = cheerio.load(html);
    var rows = $('#printable > table > tr');

    json.metadata.url = url
    json.metadata.date = new Date();
    json.temperature.average = parseFloat(rows.eq(2).find('td').eq(1).text());
    json.temperature.maximum = parseFloat(rows.eq(3).find('td').eq(1).text());
    json.temperature.minimum = parseFloat(rows.eq(4).find('td').eq(1).text());
    json.rain.amount = parseFloat(rows.eq(2).find('td').eq(6).text());
    json.rain.duration = parseFloat(rows.eq(3).find('td').eq(6).text());
    json.sky.sunshine.duration = parseFloat(rows.eq(7).find('td').eq(1).text());
    json.sky.sunshine.relative = parseInt(rows.eq(8).find('td').eq(1).text());
    json.sky.coverage = parseInt(rows.eq(9).find('td').eq(1).text());
    json.sky.visibiliy = parseFloat(rows.eq(11).find('td').eq(1).text());
    json.wind.average = parseFloat(rows.eq(7).find('td').eq(6).text());
    json.wind.maximum.average = parseFloat(rows.eq(8).find('td').eq(6).text());
    json.wind.maximum.absolute = parseFloat(rows.eq(9).find('td').eq(6).text());
    json.wind.direction = parseInt(rows.eq(11).find('td').eq(6).text());
    json.atmosphere.humidity = parseInt(rows.eq(14).find('td').eq(1).text());
    json.atmosphere.pressure = parseFloat(rows.eq(14).find('td').eq(6).text());

    // TODO check for null's

    callback(null, json);
  });

}

get_weather_object(-1, function(err, json) {
  console.log(JSON.stringify(json, null, '  '));

  var databaseUrl = 'mongodb://dbuser:dbpass@ds029960.mongolab.com:29960/weatherik'
  var collections = ['data_knmi'];
  var db = mongo.connect(databaseUrl, collections);
  db.data_knmi.save(json, function(err, saved) {
    if (err || !saved) {
      console.error('Failed saving data');
      system.exit(1); // TODO
    } else {
      console.log('Stored in database');
      system.exit(0); // TODO
    }
  });
});

