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

var prepareDBCollection = function() {
  throw("Not yet implemented")
}

var storeData = function(data) {
  console.dir(data);
}

var parseLink = function(link) {
  download(link, function(data) {
    if(data) {
      var result = {}
        , $ = cheerio.load(data);
      result["URL"] = link;
      result["is_city"] = true;

      // TODO Investigate support for all jQuery filters

      // result["population"] = $('table.infobox.geography.vcard th:contains(Population)').parent().next().find('th:contains(Total)')//.next().text();
      // var census_date = $('table.infobox.geography.vcard th:contains(Population)').
                          // text().match(/(\d{4})-(\d{2})-(\d{2})/);
      // result["census_date"] = new Date(census_date[1], census_date[2] - 1, census_date[3]);
      // result["coords"] = { latitude : $('table.infobox.geography.vcard td:contains(Coordinates) span.latitude').first().text(), // bad selector, investigate
                           // longtitude : $('table.infobox.geography.vcard td:contains(Coordinates) span.longitude').first().text()
                         // };

      result["last_crawled"] = new Date();
      storeData(result);
    } else {
      console.dir("Could not get data for link: " + link);
    }
  });
}


var parseLinks = function(data) {
  for(var i = 0; i < data.length; i++) {
    parseLink(data[i]);
  }
  return;
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

// Opening connection to a database and creating necessary collections
// prepareDBCollection();

// Getting links using provided time interval
if(argv.hasOwnProperty("t")) {
  setInterval(get_links, argv.t * 1000);
} else {
  console.dir("Please set time interval in seconds with -t option")
}
