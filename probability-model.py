# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 21:23:11 2015

@author: daviz
"""
import pandas as pd
import numpy as np
import pygeoj
import pymongo

# Connection to Mongo DB
try:
    conn=pymongo.MongoClient()
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e

conn.drop_database("merchant_zipcode_aggregation")
conn.drop_database("merchant_zipcode_coordinates")

db = conn['merchant_zipcode_aggregation']
db = conn['merchant_zipcode_coordinates']

# Load datasets
names = ["merchant_zipcode", "date", "category", "age_interval", "gender", "merchants", "cards", "payments", "avg_payment", "max_payment", "min_payment", "std"]
demo_stats = pd.read_csv("dataset/demographic_distribution000", delim_whitespace=True, names= names, parse_dates=["date"], dtype = {'merchant_zipcode': str})

bcn_zipcodes = ['08001', '08002', '08003', '08004', '08005', '08006', '08007',
                '08008', '08009', '08010', '08011', '08012', '08013', '08014',
                '08015', '08016', '08017', '08018', '08019', '08020', '08021',
                '08022', '08023', '08024', '08025', '08026', '08027', '08028',
                '08029', '08030', '08031', '08032', '08033', '08034', '08035',
                '08036', '08037', '08038', '08039', '08040', '08041', '08042']

demo_stats = demo_stats[demo_stats.merchant_zipcode.apply(lambda zp: zp in bcn_zipcodes)]

demo_stats = demo_stats.loc[demo_stats["gender"] != 'unknown']
demo_stats = demo_stats.loc[demo_stats["age_interval"] != 'unknown']

demo_stats = demo_stats[demo_stats.category == 'es_barsandrestaurants']

demo_stats["weekday"] = demo_stats["date"].map(lambda d: (d.weekday()))
demo_stats["weekday"] = demo_stats["weekday"].astype('string')

gbcn = demo_stats.groupby(["gender", "age_interval", "weekday", "merchant_zipcode"]).aggregate({ "payments": np.sum })

gbcn = gbcn.reset_index()
total = demo_stats["payments"].sum()
gbcn['payments_proportion'] = gbcn.payments / total

zip_code_geojson = pygeoj.load(filepath="dataset/cp_cat_merchant_zipcode.geojson")

for feature in zip_code_geojson:
    zipcode = feature.properties['merchant_zipcode']
    db.merchant_zipcode_coordinates.insert({'merchant_zipcode': zipcode,
                                            'coordinates': feature.geometry.coordinates })

db.merchant_zipcode_aggregation.insert(gbcn.to_dict("records"))

records = db.merchant_zipcode_aggregation.find({ "age_interval": "35-44",
                                                 "gender": "male",
                                                 "weekday": "5" }).sort("payments_proportion", pymongo.DESCENDING).limit(5)

for row in records:
    print row['merchant_zipcode']
    print row['payments_proportion']

records.rewind()
zipcode = records.next()
merchant_zipcode = zipcode['merchant_zipcode']
payment_proportion = zipcode['payments_proportion']

record = db.merchant_zipcode_coordinates.find({ "merchant_zipcode": merchant_zipcode })
print record.next()