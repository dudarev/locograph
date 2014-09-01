// TODO 1
// Now we keep all code and variables together
// should be refactored and be split unto different files

// Variables area

var http = require("http")
    , cheerio = require("cheerio")
    , MongoClient = require('mongodb').MongoClient;

var cities_url = "http://en.wikipedia.org/wiki/List_of_towns_and_cities_with_100,000_or_more_inhabitants/cityname:_A"
    , base_url = "http://en.wikipedia.org"
    , city_links = [];

// Functions area

// Utility function that downloads a URL and invokes
// callback with the data.
var download = function(url, callback) {
  http.get(url, function(res) {
    var data = "";
    res.on('data', function (chunk) {
      data += chunk;
    });
    res.on("end", function() {
      callback(data);
    });
  }).on("error", function() {
    callback(null);
  });
}

// Get links from the cities ulr, using JQuery-like syntax
// In 'usual' JQuery the request would be
// ``````

var get_links = function() {
  download(cities_url, function(data) {
    if(data) {
      var $ = cheerio.load(data);
      var result = $('table.wikitable tr td:not(:has(>span)) a').map(function(i, el) {
        return base_url + $(el).attr('href');
      });
      return result;
    } else {
      throw "Could not dowload data from given url"
    }
  });
}


// main part
// TODO 2 move into loop

get_links();
