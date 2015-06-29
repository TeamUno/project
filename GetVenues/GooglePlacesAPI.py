# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 14:16:21 2015

@author: diego
"""

from googleplaces import GooglePlaces, types, ranking
import json
import pandas as pd
import urllib
import urllib2

import pymongo


def _fetch_remote(service_url, params={}, use_http_post=False):
    encoded_data = {}
    for k, v in params.items():
        if type(v) in [str, unicode]:
            v = v.encode('utf-8')
        encoded_data[k] = v
    encoded_data = urllib.urlencode(encoded_data)

    if not use_http_post:
        query_url = (service_url if service_url.endswith('?') else
                     '%s?' % service_url)
        request_url = query_url + encoded_data
        request = urllib2.Request(request_url)
    else:
        request_url = service_url
        request = urllib2.Request(service_url, data=encoded_data)
    return (request_url, urllib2.urlopen(request))

def _fetch_remote_json(service_url, params={}, use_http_post=False):
    """Retrieves a JSON object from a URL."""
    request_url, response = _fetch_remote(service_url, params, use_http_post)
    return (request_url, json.load(response))
    

# Connection to Mongo DB
try:
    conn=pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e

db = conn['TeamUno']
venues=db.venuesGooglePlaces
venues.create_index('place_id',unique=True) #el índice será el place_id del venue, y unique=True no nos dejará insertar duplicados

YOUR_API_KEY = '' # utilizad la llave de g1datascienceub (https://console.developers.google.com/project/letmeguess-989/apiui/credential?authuser=0)
placesapiurl='https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
detailapiurl='https://maps.googleapis.com/maps/api/place/details/json?'

google_places = GooglePlaces(YOUR_API_KEY)

centroides=open('/Users/diego/Desktop/Centroids/centroidsok.csv','r')
locations=pd.read_csv(centroides)
locations.rename(columns={'long':'lng'},inplace=True)


# Barro primero 4π km^2 alrededor de cada centroide de los CP de merchant_zipcode que tenemos
# y obtengo una lista de "hasta" 60 (20+20+20), ordenador por un indicator propio de Google (PROMINENCE).
# También utilizo como filtro los que cuadren con la categoría Bar&Restaurant

for i in range(0,locations.shape[0]):
    query_result = google_places.nearby_search(
            lat_lng=locations.ix[i][['lat','lng']].to_dict(),
            rankby=ranking.PROMINENCE,
            radius=2000, types=[types.TYPE_FOOD,
                                types.TYPE_BAR,
                                types.TYPE_CAFE,
                                types.TYPE_MEAL_TAKEAWAY,
                                types.TYPE_MEAL_DELIVERY,
                                types.TYPE_RESTAURANT])
    for place in query_result.places:
        try:
            venues.insert(_fetch_remote_json(detailapiurl+'placeid='+place.place_id+'&key='+YOUR_API_KEY,use_http_post=True)[1]['result'])
        except:
            continue
    try:
        nexttoken=query_result.raw_response['next_page_token']
        nextpage=_fetch_remote_json(placesapiurl+'pagetoken='+nexttoken+'&key='+YOUR_API_KEY,use_http_post=True)[1]
        for place in nextpage['results']:
            try:
                venues.insert(_fetch_remote_json(detailapiurl+'placeid='+place['place_id']+'&key='+YOUR_API_KEY,use_http_post=True)[1]['result'])
            except:
                continue
        try:
            nexttoken=nextpage['next_page_token']
            nextpage=_fetch_remote_json(placesapiurl+'pagetoken='+nexttoken+'&key='+YOUR_API_KEY,use_http_post=True)[1]
            for place in nextpage['results']:
                try:
                    venues.insert(_fetch_remote_json(detailapiurl+'placeid='+place['place_id']+'&key='+YOUR_API_KEY,use_http_post=True)[1]['result'])
                except:
                    continue
        except:
            continue
    except:
        continue

# Por si hay códigos postales con pocos bar&restaurants en los 4π km^2 alrededor del centroide, hago otro barrido, pero
# esta vez con DISTANCE. Ahora obtendré los 60 (20+20+20) que estén más cerca del centroide, sin límite de distancia. Con estos dos
# barridos deberíamos haber pillado todo lo necesario.

for i in range(0,locations.shape[0]):
    query_result = google_places.nearby_search(
            lat_lng=locations.ix[i][['lat','lng']].to_dict(),
            rankby=ranking.DISTANCE, types=[types.TYPE_FOOD,
                                types.TYPE_BAR,
                                types.TYPE_CAFE,
                                types.TYPE_MEAL_TAKEAWAY,
                                types.TYPE_MEAL_DELIVERY,
                                types.TYPE_RESTAURANT])
    for place in query_result.places:
        try:
            venues.insert(_fetch_remote_json(detailapiurl+'placeid='+place.place_id+'&key='+YOUR_API_KEY,use_http_post=True)[1]['result'])
        except:
            continue
    try:
        nexttoken=query_result.raw_response['next_page_token']
        nextpage=_fetch_remote_json(placesapiurl+'pagetoken='+nexttoken+'&key='+YOUR_API_KEY,use_http_post=True)[1]
        for place in nextpage['results']:
            try:
                venues.insert(_fetch_remote_json(detailapiurl+'placeid='+place['place_id']+'&key='+YOUR_API_KEY,use_http_post=True)[1]['result'])
            except:
                continue
        try:
            nexttoken=nextpage['next_page_token']
            nextpage=_fetch_remote_json(placesapiurl+'pagetoken='+nexttoken+'&key='+YOUR_API_KEY,use_http_post=True)[1]
            for place in nextpage['results']:
                try:
                    venues.insert(_fetch_remote_json(detailapiurl+'placeid='+place['place_id']+'&key='+YOUR_API_KEY,use_http_post=True)[1]['result'])
                except:
                    continue
        except:
            continue
    except:
        continue