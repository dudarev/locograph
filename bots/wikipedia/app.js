// TODO 1
// Now we keep all code and variables together
// should be refactored and be split unto different files

// Variables area

var http = require("http")
    , cheerio = require("cheerio")
    , MongoClient = require('mongodb').MongoClient
    , argv = require('minimist')(process.argv.slice(2));

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

var parseLinks = function(data) {
  console.dir(data);
  return data;
}

var store = function(data) {
  console.dir(data);
  return data;
}

// Get links from the cities url, using JQuery-like syntax

var get_links = function() {
  console.dir("Getting data...");
  download(cities_url, function(data) {
    if(data) {
      var $ = cheerio.load(data);
      var result = $('table.wikitable tr td:not(:has(>span)) a').map(function(i, el) {
        return base_url + $(el).attr('href');
      });
      parseLinks(result);
    } else {
      throw "Could not dowload data from given url"
    }
  });
}


// main part

// Getting links using provided time interval
if(argv.hasOwnProperty("t")) {
  setInterval(get_links, argv.t * 1000);
} else {
  console.dir("Please set time interval in seconds with -t option")
}
