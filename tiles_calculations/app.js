
var ZOOM_LEVELS = [1, 2, 3, 4, 5, 6, 7, 8 , 9, 10,
                   11, 12, 13, 14, 15, 16, 17, 18]
  , EARTH_RADIUS = 6371;


var slipplyTileSize = function(lontit_degree, lat_degree, zoom) {
  var km_per_lontitude = 2 * Math.PI * EARTH_RADIUS * Math.cos(lat_degree) / 360;
  var km_per_latitude = 2 * Math.PI * EARTH_RADIUS / 360;
  var tile_size_in_degrees = { x: 360/Math.pow(2, zoom),
                               y: 170.1022/Math.pow(2, zoom) };
  return [tile_size_in_degrees.x * km_per_lontitude,
          tile_size_in_degrees.y * km_per_latitude]
}

var quadTileSize = function(lontit_degree, lat_degree, zoom) {
  // pending
  return;
}

// main part

console.log('SLIPPY TILES');
console.log('0 degrees');
for(var i in ZOOM_LEVELS) {
  var res = slipplyTileSize(0, 0, ZOOM_LEVELS[i]);
  console.log('zoom_level: ' + ZOOM_LEVELS[i] + '\tw: ' + res[0] + ', h: ' + res[1]);
}

console.log('45 degrees');
for(var i in ZOOM_LEVELS) {
  var res = slipplyTileSize(0, 45, ZOOM_LEVELS[i]);
  console.log('zoom_level: ' + ZOOM_LEVELS[i] + '\tw: ' + res[0] + ', h: ' + res[1]);
}
