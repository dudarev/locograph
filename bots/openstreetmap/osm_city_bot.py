from datetime import datetime
import os
import subprocess

from imposm.parser import OSMParser


# EXTRACT_URL = "https://s3.amazonaws.com/metro-extracts.mapzen.com/odessa.osm.bz2"
EXTRACT_URL = "map.osm"
FILENAME = EXTRACT_URL.split('/')[-1]


if not os.path.exists(FILENAME):
    print 'downloading file'
    subprocess.call(['wget', EXTRACT_URL])
else:
    print 'file exists'


class Place(object):
    """Place can be a node, a way or a relation.
    """

    def __init__(self, name, coordinates=None, tags=None, refs=None, members=None):
        self.name = name
        self.coordinates = coordinates
        self.tags = tags
        self.refs = refs
        self.memebers = members
        self.last_crawled = datetime.utcnow()

    def update_coordinates(self):
        """If a place does not have coordinates, tries to update them from refs or members.
        Coordinates are calculated as a center of bounding box.
        """
        if not self.coordinates:
            if self.refs:
                self.coordinates = self.find_bounding_box(self.refs)
            elif self.members:
                self.coordinates = self.find_bounding_box(self.members)


# simple class that handles parsed OSM data
class PlaceCollector(object):
    ways_count = 0
    nodes_count = 0
    relations_count = 0
    nodes = []
    ways = []
    relations = []

    def nodes(self, nodes):
        for osmid, tags, coords in nodes:
            if 'place' in tags:
                self.nodes_count += 1

    def ways(self, ways):
        for osmid, tags, refs in ways:
            if 'place' in tags:
                self.ways_count += 1

    def relations(self, relations):
        for osmid, tags, members in relations:
            if 'place' in tags:
                print members
                self.relations_count += 1


if __name__ == '__main__':

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

    # save populated places in MongoDB
    # for p in places:
    #     p.save()
