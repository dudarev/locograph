import os
import subprocess

URL = "http://download.geofabrik.de/europe/ukraine-latest.osm.pbf"
file_name = URL.split('/')[-1]

if os.path.exists(file_name):
    print 'file already exists'
else:
    subprocess.call(['wget', URL])
