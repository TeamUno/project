# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 19:49:54 2015

@author: diego
"""

from geopy.geocoders import Nominatim
import pymongo
import re
#import numpy as np
#from operator import itemgetter, attrgetter

# Connection to Mongo DB
try:
    conn = pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure as error:
    print "Could not connect to MongoDB: %s" % error

db = conn['TeamUno']
venuesFS = db.venuesFoursquareCAT

# COn este código obtengo el zipcode de muchos de los venues de los que FS no 
# me lo daba, ¡¡recuperando más de 700!!
geolocator = Nominatim()
for u in venuesFS.find({u'zipcode': {'$eq': None}}):
    try:
        u['zipcode'] = re.search(r'\d{5}', geolocator.reverse(str(u['latitude']) + ',' + str(u['longitude'])).address).group(0)
    except:
        continue
    venuesFS.save(u)