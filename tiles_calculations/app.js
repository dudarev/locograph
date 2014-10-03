var __hasProp = {}.hasOwnProperty;

var __extends = function(child, parent) {
  for (var key in parent) {
    if (__hasProp.call(parent, key)) { child[key] = parent[key]; }
  }
  function ctor() { this.constructor = child; }
  ctor.prototype = parent.prototype;
  child.prototype = new ctor();
  child.__super__ = parent.prototype;
  return child;
};

var TileSize = (function() {
  function TileSize(lontit_degree, lat_degree) {
    this.lontit_degree = lontit_degree;
    this.lat_degree = lat_degree;
    this.zoomLevels = [1, 2, 3, 4, 5, 6, 7, 8 , 9, 10,
                       11, 12, 13, 14, 15, 16, 17, 18];
    this.earthRadius = 6371;
  }

  TileSize.prototype.sizeDegrees = function() {
    throw 'Not Implemented!'
  }

  TileSize.prototype.sizeKilometers = function() {
    throw 'Not Implemented!'
  }

  TileSize.prototype.results = function() {
    console.log(this.lat_degree + ' degrees');
    for(var i in this.zoomLevels) {
      var zoomLevel = this.zoomLevels[i];
      var res = this.sizeKilometers(zoomLevel);
      console.log('zoom_level: ' + zoomLevel + '\tw: ' + res.width + ', h: ' + res.height);
    }
  }

  return TileSize;
})();

var QuadTileSize = (function(_super) {
   __extends(QuadTileSize, _super);

   function QuadTileSize() {
    return QuadTileSize.__super__.constructor.apply(this, arguments);
  }

  QuadTileSize.prototype.sizeDegrees = function(zoom) {
    return { x: 360.0/Math.pow(2, zoom),
             y: 180.0/Math.pow(2, zoom) };

  };

  QuadTileSize.prototype.sizeKilometers = function(zoom) {
    var km_per_latitude = 2 * Math.PI * this.earthRadius / 360.0;
    var km_per_lontitude = 2 * Math.PI * this.earthRadius * Math.cos(this.lat_degree) / 360.0;
    var tile_size_in_degrees = this.sizeDegrees(zoom);

    return {width: tile_size_in_degrees.x * km_per_lontitude,
            height: tile_size_in_degrees.y * km_per_latitude
           }
  };

  return QuadTileSize;
})(TileSize);


var quadTile = new QuadTileSize(0, 0);
quadTile.results();
