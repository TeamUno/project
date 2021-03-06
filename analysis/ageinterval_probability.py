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

db.drop_collection("ageinterval_aggregation")

# Load datasets
names = ["merchant_zipcode", "date", "category", "ageinterval", "merchants", "cards", "payments", "avg_payments", "max_payments", "min_payments", "std"]
ageinterval_stats = pd.read_csv("../dataset/age_distribution000",  delim_whitespace=True, names= names, parse_dates=["date"], dtype = {'merchant_zipcode': str})

bcn_zipcodes = ['08001', '08002', '08003', '08004', '08005', '08006', '08007',
                '08008', '08009', '08010', '08011', '08012', '08013', '08014',
                '08015', '08016', '08017', '08018', '08019', '08020', '08021',
                '08022', '08023', '08024', '08025', '08026', '08027', '08028',
                '08029', '08030', '08031', '08032', '08033', '08034', '08035',
                '08036', '08037', '08038', '08039', '08040', '08041', '08042']

ageinterval_stats = ageinterval_stats[ageinterval_stats.merchant_zipcode.apply(lambda zp: zp in bcn_zipcodes)]
ageinterval_stats = ageinterval_stats[ageinterval_stats.ageinterval != 'unknown']
ageinterval_stats = ageinterval_stats[ageinterval_stats.category == 'es_barsandrestaurants']

def laplace_correction(payments, total_payments, beta):
    return ( payments + 1. ) / (total_payments + beta)


gbcn = ageinterval_stats.groupby(["ageinterval", "merchant_zipcode"]).aggregate({ "payments": np.sum })
gbcn = gbcn.reset_index()

total_payments = gbcn.payments.sum()

proba_list = []
age_interval_list = list(ageinterval_stats.ageinterval.unique())
beta = len(age_interval_list) * len(bcn_zipcodes)
for zipcode in bcn_zipcodes:
    for age_interval in age_interval_list:
        proba = {}
        proba["merchant_zipcode"] = zipcode
        proba["ageinterval"] = age_interval
        row = gbcn[(gbcn.ageinterval == age_interval) & (gbcn.merchant_zipcode == zipcode)]
        if len(row) == 1 :
          payments = int(row.payments)
        else:
          payments = 0
        proba["payments_proportion"] = laplace_correction(payments,total_payments, beta)
        proba_list.append(proba)


db.ageinterval_aggregation.insert(proba_list)
