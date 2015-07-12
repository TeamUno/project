# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 21:23:11 2015

@author: daviz
"""
import pandas as pd
import numpy as np
import pymongo

# Connection to Mongo DB
try:
    client = pymongo.MongoClient()
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e

db = client['wherelocalsgo']

db.drop_collection("weekday_aggregation")

# Load datasets
names = ["merchant_zipcode", "date", "category", "merchants", "cards", "payments", "avg_payments", "max_payments", "min_payments", "std"]
weekdaystats = pd.read_csv("../dataset/basic_stats000",  delim_whitespace=True, names= names, parse_dates=["date"], dtype = {'merchant_zipcode': str})
weekdaystats["weekday"] = weekdaystats["date"].map(lambda d: (d.weekday()))

bcn_zipcodes = ['08001', '08002', '08003', '08004', '08005', '08006', '08007',
                '08008', '08009', '08010', '08011', '08012', '08013', '08014',
                '08015', '08016', '08017', '08018', '08019', '08020', '08021',
                '08022', '08023', '08024', '08025', '08026', '08027', '08028',
                '08029', '08030', '08031', '08032', '08033', '08034', '08035',
                '08036', '08037', '08038', '08039', '08040', '08041', '08042']

weekdaystats = weekdaystats[weekdaystats.merchant_zipcode.apply(lambda zp: zp in bcn_zipcodes)]
weekdaystats = weekdaystats[weekdaystats.category == 'es_barsandrestaurants']

def laplace_correction(payments, total_payments, beta):
    return ( payments + 1. ) / (total_payments + beta)



gbcn = weekdaystats.groupby(["weekday", "merchant_zipcode"]).aggregate({ "payments": np.sum })
gbcn = gbcn.reset_index()

total_payments = gbcn.payments.sum()
proba_list = []
weekdays_list = range(0,7)
beta = len(weekdays_list) * len(bcn_zipcodes)
for zipcode in bcn_zipcodes:
    for weekday in weekdays_list:
        proba = {}
        proba["merchant_zipcode"] = zipcode
        proba["weekday"] = weekday
        row = gbcn[(gbcn.weekday == weekday) & (gbcn.merchant_zipcode == zipcode)]
        if len(row) == 1 :
          payments = int(row.payments)
        else:
          payments = 0
        proba["payments_proportion"] = laplace_correction(payments,total_payments, beta)
        proba_list.append(proba)


db.weekday_aggregation_prob.insert(proba_list)
