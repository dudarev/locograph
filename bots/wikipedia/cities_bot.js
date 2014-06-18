

var links = [];
var cities_url = "http://en.wikipedia.org/wiki/List_of_towns_and_cities_with_100,000_or_more_inhabitants/cityname:_A";
var base_url = 'http://en.wikipedia.org/';
var casper = require('casper').create();

function getLinks() {
  var links = document.querySelectorAll('table tbody tr td a');
  return Array.prototype.map.call(links, function(e) {
    return e.getAttribute('href');
  });
}

casper.start(cities_url, function() {
  links = links.concat(this.evaluate(getLinks));
});

casper.run(function() {
  this.echo(links.length + 'cities found:');
  this.echo(' - ' + links.join('\n - ')).exit();
});
