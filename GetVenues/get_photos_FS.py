# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 00:30:34 2015

@author: diego
"""


import foursquare as fq
import pymongo

# Connection to Mongo DB
try:
    conn=pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e 


db = conn['wherelocalsgo']
venues=db.places

client = fq.Foursquare(
            client_id = 'UNPSIQJAFMS0TZXGSMDQETOEDBJHI0YOFSXILBB5OS1VXPKX',
            client_secret = 'DV0PLC2R1YEN50VKDRIJS2M1QRO5X2FOMKHIFSL20BKOSUWB')


for u in venues.find():
    if client.venues(u['id'])['venue']['photos']['count'] != 0 :
        photo_url_splitted = client.venues.photos(u['id'], {}, multi=False)['photos']['items'][0]
        size = 'original' # other sizes available: https://developer.foursquare.com/docs/responses/photo.html
        u['photo_url'] = photo_url_splitted['prefix'] + size + photo_url_splitted['suffix']
        venues.save(u)