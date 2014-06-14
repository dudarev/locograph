import os
import subprocess

extract_url = "https://s3.amazonaws.com/metro-extracts.mapzen.com/odessa.osm.bz2"
filename = extract_url.split('/')[-1]

if not os.path.exists(filename):
    subprocess.call(['wget', extract_url])
else:
    print 'file exists'

# loop over entities and extract pois
# save populated places in MongoDB
