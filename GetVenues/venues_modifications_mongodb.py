# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
Created on Fri Jun 26 16:37:13 2015

@author: diego
"""

import pymongo
#import re
#import numpy as np
#from operator import itemgetter, attrgetter


# Connection to Mongo DB
try:
    conn = pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure as error:
    print "Could not connect to MongoDB: %s" % error

db = conn['TeamUno']
venuesGP = db.venuesGooglePlaces
venuesFS = db.venuesFoursquare

#for u in venuesFS.find():
#    if u['merchant_zipcode'] != None:
#        u['merchant_zipcode'] = u['merchant_zipcode'].zfill(5)
#        if len(u['merchant_zipcode']) > 5 or not u['merchant_zipcode'].isdigit():
#            u['merchant_zipcode'] = None
#    venuesFS.save(u)

## ------------------------------------------------------------------
## Extract ZIP from formatted address field and adds a new key zipcode:ZIP
## ------------------------------------------------------------------
#
#for u in venuesGP.find({u'formatted_address': {'$regex': '\d{5}'}}):
#    u['zipcode'] = re.search(r'\d{5}', u['formatted_address']).group(0)
#    venuesGP.save(u)

## ------------------------------------------------------------------
## Get only the categories related to Bars and Restaurants
## ------------------------------------------------------------------
#
##Get all categories
#
#data = [u['category'] for u in venuesFS.find({}, {'category': 1})]
#
##Count them
#
#data = dict((x, data.count(x)) for x in data)
#
##Sort the categories per appearances
#
#a = sorted([[key, value] for key, value in data.iteritems()],
# key = itemgetter(1), reverse=True)
#
# Save to a list to check manually on Excel if the category fits in
#Bar&Restaurant
#
#writer = csv.writer(open("categories.csv", 'w'))
#for row in a:
#    writer.writerow([unicode(s).encode("utf-8") for s in row])
#
## Fits in or not
#
#catfilt = [1,1,1,1,1,0,1,0,0,1,0,1,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,0,0,1,0,1,0,
#0,0,1,0,0,1,0,0,1,1,1,1,1,0,0,0,1,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,1,0,0,1,0,0,
#0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,
#0,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,0,0,1,0,1,0,0,0,
#0,0,0,1,1,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,1,0,1,0,0,0,0,1,1,1,0,1,0,0,0,0,
#1,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,
#1,0,0,0,1,1,0,0,0,1,0,1]
#b=[]
#for i in range(0, len(a)):
#    if catfilt[i] == 1:
#        b.append(a[i][0])
#
##Categories in the dataset that fit
#
#b = [u'Mediterranean Restaurant', u'Restaurant', u'Caf\xe9',
# u'Spanish Restaurant', u'Tapas Restaurant', u'Bar', u'Pizza Place',
# u'Italian Restaurant', u'Coffee Shop', u'Fast Food Restaurant',
# u'Cocktail Bar', u'Seafood Restaurant', u'Nightclub', u'Burger Joint',
# u'Ice Cream Shop', u'Sandwich Place', u'Diner', u'Breakfast Spot', u'Food',
# u'Japanese Restaurant', u'Pub', u'Sporting Goods Shop', u'Paella Restaurant',
# u'Snack Place', u'BBQ Joint', u'Gastropub', u'Chinese Restaurant',
# u'Brewery',
# u'American Restaurant', u'Asian Restaurant', u'Sushi Restaurant',
# u'Argentinian Restaurant', u'Steakhouse', u'Hot Dog Joint',
# u'Mexican Restaurant', u'Beach Bar', u'Wine Bar', u'French Restaurant',
# u'Vegetarian / Vegan Restaurant', u'Ramen / Noodle House',
# u'Fried Chicken Joint', u'Falafel Restaurant', u'Hotel Bar',
# u'Turkish Restaurant', u'Tea Room', u'Food Court', u'Cafeteria', u'Bistro',
# u'Indian Restaurant', u'Kebab Restaurant', u'Caribbean Restaurant',
# u'Food Truck', u'Frozen Yogurt', u'Thai Restaurant', u'Comedy Club',
# u'Gay Bar', u'Molecular Gastronomy Restaurant', u'Dive Bar', u'Creperie',
# u'Hookah Bar', u'Middle Eastern Restaurant', u'German Restaurant',
# u'Gluten-free Restaurant', u'Juice Bar', u'Pakistani Restaurant',
# u'Korean Restaurant', u'Salad Place', u'New American Restaurant',
# u'Peruvian Restaurant', u'Home Cooking Restaurant', u'Buffet',
# u'Karaoke Bar',
# u'Greek Restaurant', u'Burrito Place', u'English Restaurant',
# u'Latin American Restaurant', u'Whisky Bar', u'Irish Pub',
# u'Vietnamese Restaurant', u'Taco Place', u'Piano Bar']
#
#dataCAT = [u for u in venuesFS.find({'category': {'$in': b}})]
#for u in venuesFS.find({'category': {'$in': b}}):
#    u['supercategory'] = 'bars_and_restaurants'
#    venuesFS.save(u)
#for u in venuesFS.find({'category': {'$nin': b}}):
#    u['supercategory'] = 'others'
#    venuesFS.save(u)

## ------------------------------------------------------------------
## Get only the venues with zipcode, rating and price, and normalize price and
## rating
## ------------------------------------------------------------------
#
#db.venuesFS_filter.insert_many([u for u in venuesFS.find({'$and':[
#{'rating': {'$ne': None}}, {'category': {'$in':b}}, {'price': {'$ne': None}},
#{'merchant_zipcode': {'$regex': '\d{5}'}}]})])

#db.venuesGP_filter.insert_many([u for u in venuesGP.find({'$and':[
#{'rating': {'$exists': 'true'}}, {'formatted_address': {'$regex': '\d{5}'}},
#{'types': {'$nin': ['store']}}, {'price_level': {'$exists': 'true'}}]})])
#
#for u in db.venuesFS_filter.find():
#    u['price_norm'] = (u['price']-1)/3.
#    u['rating_norm'] = u['rating']/10.
#    db.venuesFS_filter.save(u)
#
#for u in db.venuesGP_filter.find():
#    u['price_norm'] = u['price_level']/4.
#    u['rating_norm'] = (u['rating']-1)/4.
#    db.venuesGP_filter.save(u)
