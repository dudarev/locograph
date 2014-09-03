"""
Extracts osm data for bounding boxes specified in cities.csv.
"""

import csv
import os
import subprocess


f = open('cities.csv')
reader = csv.reader(f)
header = reader.next()
print header

for row in reader:
    city = {}
    for k, v in zip(header, row):
        k = k.strip()
        v = v.strip().lower()
        if not k == 'name':
            v = float(v)
        city[k] = v
    print city['name']
    filename = '{}.osm.bz2'.format(city['name'])
    if os.path.exists(filename):
        print 'file exists'
    else:
        print 'extracting data'
        command = '''osmosis \
            --read-pbf file=ukraine-latest.osm.pbf \
            --bounding-box top={} left={} bottom={} right={} \
            --write-xml file=- \
            | bzip2 > {}.osm.bz2'''.format(
            city['lat_max'], city['lon_min'], city['lat_min'], city['lon_max'],
            city['name'])
        print command
        subprocess.check_call(
            command,
            shell=True
        )
