import os
import subprocess

from imposm.parser import OSMParser


extract_url = "https://s3.amazonaws.com/metro-extracts.mapzen.com/odessa.osm.bz2"
filename = extract_url.split('/')[-1]

if not os.path.exists(filename):
    subprocess.call(['wget', extract_url])
else:
    print 'file exists'

# loop over entities and extract pois


# simple class that handles the parsed OSM data.
class PlaceCounter(object):
    ways_count = 0
    nodes_count = 0
    relations_count = 0

    def ways(self, ways):
        for osmid, tags, refs in ways:
            if 'place' in tags:
                print tags['place']
                self.ways_count += 1

    def nodes(self, nodes):
        for osmid, tags, coords in nodes:
            if 'place' in tags:
                print tags['place']
                self.nodes_count += 1

    def relations(self, relations):
        for osmid, tags, members in relations:
            if 'place' in tags:
                print tags['place']
                self.relations_count += 1


# instantiate counter and parser and start parsing
counter = PlaceCounter()
p = OSMParser(
    concurrency=4,
    nodes_callback=counter.nodes,
    ways_callback=counter.ways,
    relations_callback=counter.relations)
p.parse(filename)

# done
print 'Number of nodes, ways, relations corresponding to populated places'
print 'nodes: ', counter.nodes_count
print 'ways: ', counter.ways_count
print 'relations: ', counter.relations_count

# save populated places in MongoDB
