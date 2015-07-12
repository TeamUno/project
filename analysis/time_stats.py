# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 02:53:48 2015

@author: diego based on @daviz
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

db.drop_collection("time_aggregation")
db.drop_collection("time_aggregation_prob")

# Load datasets
names = ["merchant_zipcode", "date", "day_of_week", "hour",  "merchants", "cards", "payments", "avg_payment", "max_payment", "min_payment", "std"]
time = pd.read_csv("../dataset/expenditure-time_curve000", delim_whitespace=True, names=names, parse_dates=["date"])
time["merchant_zipcode"]=time["merchant_zipcode"].apply(lambda x: str(x).zfill(5))
time["weekday"] = time["date"].map(lambda d: (d.weekday()))

names = ["merchant_zipcode", "date", "category", "merchants", "cards", "payments", "avg_payments", "max_payments", "min_payments", "std"]
basics = pd.read_csv("../dataset/basic_stats000",  delim_whitespace=True, names= names, parse_dates=["date"], dtype = {'merchant_zipcode': str})
basics["weekday"] = basics["date"].map(lambda d: (d.weekday()))

bcn_zipcodes = ['08001', '08002', '08003', '08004', '08005', '08006', '08007',
                '08008', '08009', '08010', '08011', '08012', '08013', '08014',
                '08015', '08016', '08017', '08018', '08019', '08020', '08021',
                '08022', '08023', '08024', '08025', '08026', '08027', '08028',
                '08029', '08030', '08031', '08032', '08033', '08034', '08035',
                '08036', '08037', '08038', '08039', '08040', '08041', '08042']
                
time_list = range(0, 3)  
weekday_list = range(0, 7)              


time = time[time.merchant_zipcode.apply(lambda zp: zp in bcn_zipcodes)]
basics = basics[basics.merchant_zipcode.apply(lambda zp: zp in bcn_zipcodes)]

def laplace_correction(payments, total_payments, beta):
    return ( payments + 1. ) / (total_payments + beta)

def timify(hour):
    timy = 0
    if hour >= 5 and hour <= 11:
        timy = 0
    elif hour >= 12 and hour <= 17:
        timy = 1
    elif hour >= 18 or hour <= 2:
        timy = 2
    return timy

time['time']=time.apply(lambda row: timify(row['hour']), axis = 1)

gbcn_basics = basics.groupby(["weekday", "merchant_zipcode", "category"]).aggregate({ "payments": np.sum })
gbcn_basics = gbcn_basics.reset_index()
gbcn_basics = gbcn_basics[gbcn_basics['category'] == 'es_barsandrestaurants']
del gbcn_basics['category']

tots = basics.groupby(["weekday", "merchant_zipcode"]).aggregate({"payments": np.sum})
tots = tots.reset_index()


proba_list = []
beta = len(bcn_zipcodes) * len(weekday_list)
for zipcode in bcn_zipcodes:
    for weekday in weekday_list:
        proba = {}
        proba["merchant_zipcode"] = zipcode
        proba["weekday"] = weekday
        row_bars = gbcn_basics[(gbcn_basics.weekday == weekday) & (gbcn_basics.merchant_zipcode == zipcode)]
        row_tots = tots[(tots.weekday == weekday) & (tots.merchant_zipcode == zipcode)]
        proportion = int(row_bars.payments) if len(row_bars) == 1 else 0
        total = int(row_tots.payments) if len(row_tots) == 1 else 1

        proba["barsandrestaurants_proportion"] = laplace_correction(proportion,total, beta)
        proba_list.append(proba)

gbcn_basics_df = pd.DataFrame(proba_list)

gbcn = time.groupby(["weekday", "time", "merchant_zipcode"]).aggregate({ "payments": np.sum })
gbcn = gbcn.reset_index()

proba_list = []
for zipcode in bcn_zipcodes:
    for time in time_list:
        for weekday in weekday_list:
            proba = {}
            proba["merchant_zipcode"] = zipcode
            proba["weekday"] = weekday
            proba["time"] = time
            try:
                row_paym = gbcn[(gbcn.time == time) & (gbcn.weekday == weekday) & (gbcn.merchant_zipcode == zipcode)]
                row_prop = gbcn_basics_df[(gbcn_basics_df.weekday == weekday) & (gbcn_basics_df.merchant_zipcode == zipcode)]
                payments = int(row_paym.payments) if len(row_paym) == 1 else 0
                proportion = float(row_prop.barsandrestaurants_proportion) if len(row_prop) == 1 else 0
                alpha = 1. if time <= 1 else 1.25     
                proba["payments"] = int(payments * proportion * alpha)
                proba_list.append(proba)
            except:
                continue

            
gbcn_corr = pd.DataFrame(proba_list)

total_payments = gbcn_corr.payments.sum()
proba_list = []

beta = len(bcn_zipcodes) * len(time_list) * len(weekday_list)
for zipcode in bcn_zipcodes:
    for time in time_list:
        for weekday in weekday_list:
            proba = {}
            proba["merchant_zipcode"] = zipcode
            proba["time"] = time
            proba["weekday"] = weekday
            row = gbcn_corr[(gbcn_corr.weekday == weekday) & (gbcn_corr.time == time) & (gbcn_corr.merchant_zipcode == zipcode)]
            if len(row) == 1 :
              payments = int(row.payments)
            else:
              payments = 0
            proba["payments_proportion"] = laplace_correction(payments,total_payments, beta)
            proba_list.append(proba)

            
gbcn_def = pd.DataFrame(proba_list)

db.time_aggregation_prob.insert(proba_list)

