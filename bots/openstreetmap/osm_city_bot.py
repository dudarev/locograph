"""
Parses all nodes and circular ways with names. Saves them in GeoJSON format.

No relations are parsed for now. This may result in duplicates when some nodes
and ways are part of the same relation.
"""

from datetime import datetime
import os
import plyvel
from shutil import rmtree
import subprocess

import geojson
from imposm.parser import OSMParser


EXTRACT_URL = "https://s3.amazonaws.com/metro-extracts.mapzen.com/odessa.osm.bz2"
# EXTRACT_URL = "map.osm"
FILENAME = EXTRACT_URL.split('/')[-1]


if not os.path.exists(FILENAME):
    print 'downloading file'
    subprocess.call(['wget', EXTRACT_URL])
else:
    print 'file exists'


class Coords():
    def __init__(self, db):
        self.db = db

    def coord_precache(self, coords):
        for id, lat, lon in coords:
            self.db.put(str(id), str(lat) + ',' + str(lon))


class Place(object):
    """Place can be a node, a way or a relation.
    """

    def __init__(self, name, id=None, coordinates=None, tags=None, refs=None, members=None):
        self.id = id
        self.name = name
        self.coordinates = coordinates
        self.tags = tags
        self.refs = refs  # used in ways
        self.memebers = members  # used in relations
        self.last_crawled = datetime.utcnow()

    @staticmethod
    def find_bbox_center(refs):
        coords = []
        for ref in refs:
            coord = coordsDB.get(str(ref))
            if coord:
                coord = map(float, coord.split(','))
                coords.append(coord)
        if coords:
            lons = [c[0] for c in coords]
            lats = [c[1] for c in coords]
            return (
                (max(lons) + min(lons)) / 2.,
                (max(lats) + min(lats)) / 2.)
        else:
            return None

    def to_feature(self):
        if not self.coordinates:
            if self.refs:
                self.coordinates = self.find_bbox_center(self.refs)
            elif self.members:
                self.coordinates = self.find_bounding_box(self.members)
        if self.coordinates:
            point = geojson.Point(self.coordinates)
            return geojson.Feature(
                geometry=point,
                id=self.id,
                properties={"tags": self.tags, "name": self.name})
        return None


# simple class that handles parsed OSM data
class PlaceCollector(object):
    def __init__(self):
        self.places = []
        self.ways_count = 0
        self.nodes_count = 0
        self.relations_count = 0

    def nodes(self, nodes):
        for osmid, tags, coords in nodes:
            name = tags.get('name', '')
            osmid = 'node/' + str(osmid)
            if name:
                self.nodes_count += 1
                self.places.append(
                    Place(name=name, id=osmid, coordinates=coords, tags=tags))

    def ways(self, ways):
        for osmid, tags, refs in ways:
            name = tags.get('name', '')
            # circular ways with name only
            if name and len(tags) and refs[0] == refs[-1]:
                osmid = 'way/' + str(osmid)
                self.ways_count += 1
                self.places.append(
                    Place(name=name, id=osmid, tags=tags, refs=refs))

    def relations(self, relations):
        for osmid, tags, members in relations:
            # no relations are parsed for now
            if 'name' in tags:
                self.relations_count += 1

    @property
    def __geo_interface__(self):
        return geojson.FeatureCollection(
            [p.to_feature() for p in self.places])


if __name__ == '__main__':

    if os.path.isdir('coords.ldb'):
        rmtree('coords.ldb')

    coordsDB = plyvel.DB(
        'coords.ldb',
        create_if_missing=True,
        error_if_exists=True,
        write_buffer_size=1048576 * 1024)

    coords = Coords(coordsDB)
    p = OSMParser(coords_callback=coords.coord_precache)
    print 'caching all coordinates'
    p.parse(FILENAME)

    # instantiate collector and parser and start parsing
    collector = PlaceCollector()
    p = OSMParser(
        concurrency=4,
        nodes_callback=collector.nodes,
        ways_callback=collector.ways,
        relations_callback=collector.relations)
    p.parse(FILENAME)

    # done
    print 'Number of nodes, ways, relations corresponding to populated places'
    print 'nodes: ', collector.nodes_count
    print 'ways: ', collector.ways_count
    print 'relations: ', collector.relations_count

    with open('poi.json', 'w') as f:
        geojson.dump(collector, f)
