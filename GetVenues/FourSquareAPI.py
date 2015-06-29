# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 01:26:33 2015

@author: diego
"""

import foursquare as fq
import csv
import pandas as pd

import pymongo

# Connection to Mongo DB
try:
    conn=pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e 
conn

db = conn['TeamUno']
venues=db.venuesFoursquare
venues.create_index('id',unique=True) #el índice será el id del venue, y unique=True no nos dejará introducir duplicados


client = fq.Foursquare(client_id ='CLIENT_ID_FS',client_secret ='CLIENT_S_FS')

centroides=open('/Users/diego/Desktop/Centroids/centroidsok.csv','r')
locations=pd.read_csv(centroides)

Nvenues=0
offset_range= range(0,2,1)
for i in range(0,locations.shape[0]):
    j=0
    for offset in offset_range:
        response = client.venues.explore(params= {'ll': str(locations.ix[i]['lat'])+','+str(locations.ix[i]['long']),
                                                  'offset': str(offset),
                                                  'limit':'50',
                                                  'radius':'10000'})
        for groups in response['groups']:
            for group in groups['items']:
                j+=1
                venue = group['venue']
                venue_row = {'id':None, 'name': None, 'rating': None, 'price': None, 'phone': None,
                          'city': None, 'merchant_zipcode': None, 'address': None,
                          'latitude': None, 'longitude': None, 'category': None }
                venue_row['id']=venue['id']
                venue_row['name'] = venue['name']
                if 'rating' in venue:
                    venue_row['rating'] = venue['rating']
                if 'price' in venue:
                     #1 is < $10 an entree, 2 is $10-$20 an entree, 3 is $20-$30 an entree, 4 is > $30
                    venue_row['price'] = venue['price']['tier']
                if 'phone' in venue['contact']:
                    venue_row['phone']= venue['contact']['phone']
                if 'city' in venue['location']:
                    venue_row['city'] = venue['location']['city']
                if 'postalCode' in venue['location']:
                    venue_row['merchant_zipcode'] = venue['location']['postalCode']
                if 'address' in venue['location']:
                    venue_row['address'] = venue['location']['address']
                if 'lat' in venue['location']:
                    venue_row['latitude'] = venue['location']['lat']
                if 'lng' in venue['location']:
                    venue_row['longitude'] = venue['location']['lng']
                for categories in venue['categories']:
                    category_list = []
                    if 'name' in categories:
                        category_list.append(categories['name'])
                    venue_row['category'] = ",".join(category_list)

                try:
                    venues.insert(venue_row)
                except:
                    continue
