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

b = [u'Mediterranean Restaurant', u'Restaurant', u'Caf\xe9',
 u'Spanish Restaurant', u'Tapas Restaurant', u'Bar', u'Pizza Place',
 u'Italian Restaurant', u'Coffee Shop', u'Fast Food Restaurant',
 u'Cocktail Bar', u'Seafood Restaurant', u'Nightclub', u'Burger Joint',
 u'Ice Cream Shop', u'Sandwich Place', u'Diner', u'Breakfast Spot', u'Food',
 u'Japanese Restaurant', u'Pub', u'Sporting Goods Shop', u'Paella Restaurant',
 u'Snack Place', u'BBQ Joint', u'Gastropub', u'Chinese Restaurant',
 u'Brewery',
 u'American Restaurant', u'Asian Restaurant', u'Sushi Restaurant',
 u'Argentinian Restaurant', u'Steakhouse', u'Hot Dog Joint',
 u'Mexican Restaurant', u'Beach Bar', u'Wine Bar', u'French Restaurant',
 u'Vegetarian / Vegan Restaurant', u'Ramen / Noodle House',
 u'Fried Chicken Joint', u'Falafel Restaurant', u'Hotel Bar',
 u'Turkish Restaurant', u'Tea Room', u'Food Court', u'Cafeteria', u'Bistro',
 u'Indian Restaurant', u'Kebab Restaurant', u'Caribbean Restaurant',
 u'Food Truck', u'Frozen Yogurt', u'Thai Restaurant', u'Comedy Club',
 u'Gay Bar', u'Molecular Gastronomy Restaurant', u'Dive Bar', u'Creperie',
 u'Hookah Bar', u'Middle Eastern Restaurant', u'German Restaurant',
 u'Gluten-free Restaurant', u'Juice Bar', u'Pakistani Restaurant',
 u'Korean Restaurant', u'Salad Place', u'New American Restaurant',
 u'Peruvian Restaurant', u'Home Cooking Restaurant', u'Buffet',
 u'Karaoke Bar',
 u'Greek Restaurant', u'Burrito Place', u'English Restaurant',
 u'Latin American Restaurant', u'Whisky Bar', u'Irish Pub',
 u'Vietnamese Restaurant', u'Taco Place', u'Piano Bar']
#
#dataCAT = [u for u in venuesFS.find({'category': {'$in': b}})]
#for u in venuesFS.find({'category': {'$in': b}}):
#    u['supercategory'] = 'bars_and_restaurants'




for u in venuesFS.find({'$and': [{u'zipcode': {'$eq': None}},
                                {'category': {'$in': b}}]}):
    try:
        u['zipcode'] = re.search(r'\d{5}', geolocator.reverse(str(u['latitude']) + ',' + str(u['longitude'])).address).group(0)
    except:
        continue
    venuesFS.save(u)