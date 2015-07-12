# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 21:23:11 2015

@author: daviz
"""
import pandas as pd
import numpy as np
import pymongo

# Set seed
np.random.seed(123)

# Connection to Mongo DB
try:
    client = pymongo.MongoClient()
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e

db = client['wherelocalsgo']

db.drop_collection("customerzipcode_aggregation")
db.drop_collection("customerzipcode_aggregation_prob")

# Load datasets
names = ["merchant_zipcode", "date", "category", "customerzipcode", "merchants", "cards", "payments", "avg_payments", "max_payments", "min_payments", "std"]
customerzipcode_stats = pd.read_csv("../dataset/customer_zipcodes000",  delim_whitespace=True, names= names, parse_dates=["date"], dtype = {'merchant_zipcode': str,'customerzipcode': str})

bcn_zipcodes = ['08001', '08002', '08003', '08004', '08005', '08006', '08007',
                '08008', '08009', '08010', '08011', '08012', '08013', '08014',
                '08015', '08016', '08017', '08018', '08019', '08020', '08021',
                '08022', '08023', '08024', '08025', '08026', '08027', '08028',
                '08029', '08030', '08031', '08032', '08033', '08034', '08035',
                '08036', '08037', '08038', '08039', '08040', '08041', '08042']

weekday_list = range(0, 7)

customerzipcode_stats = customerzipcode_stats[customerzipcode_stats.merchant_zipcode.apply(lambda zp: zp in bcn_zipcodes)]
customerzipcode_stats.customerzipcode = customerzipcode_stats.customerzipcode.apply(lambda zp: zp if zp in bcn_zipcodes or zp =='unknown' else 'visitor')
customerzipcode_stats = customerzipcode_stats[customerzipcode_stats.customerzipcode != 'unknown']
customerzipcode_stats = customerzipcode_stats[customerzipcode_stats.category == 'es_barsandrestaurants']
customerzipcode_stats["weekday"] = customerzipcode_stats["date"].map(lambda d: (d.weekday()))

def laplace_correction(payments, total_payments, beta):
    return ( payments + 1. ) / (total_payments + beta)

gbcn = customerzipcode_stats.groupby(["weekday", "customerzipcode", "merchant_zipcode"]).aggregate({ "payments": np.sum })
gbcn = gbcn.reset_index()

total_payments = gbcn.payments.sum()

proba_list = []
customer_list = list(customerzipcode_stats.customerzipcode.unique())
beta = len(customer_list) * len(bcn_zipcodes) * len(weekday_list)
for zipcode in bcn_zipcodes:
    for customer_zipcode in customer_list:
        for weekday in weekday_list:
            proba = {}
            proba["merchant_zipcode"] = zipcode
            proba["customerzipcode"] = customer_zipcode
            proba["weekday"] = weekday
            row = gbcn[(gbcn.weekday == weekday) & (gbcn.customerzipcode == customer_zipcode) & (gbcn.merchant_zipcode == zipcode)]
            if len(row) == 1 :
              payments = int(row.payments)
            else:
              payments = 0
            proba["payments_proportion"] = laplace_correction(payments, total_payments, beta)
            proba_list.append(proba)


db.customerzipcode_aggregation.insert(proba_list)

customerzipcode_df=pd.DataFrame(proba_list)

customerzipcode_stats = pd.read_csv("../dataset/customer_zipcodes000",  delim_whitespace=True, names= names, parse_dates=["date"], dtype = {'merchant_zipcode': str,'customerzipcode': str})
customerzipcode_stats = customerzipcode_stats[customerzipcode_stats.merchant_zipcode.apply(lambda zp: zp in bcn_zipcodes)]
customerzipcode_stats.customerzipcode = customerzipcode_stats.customerzipcode.apply(lambda zp: zp if zp in bcn_zipcodes or zp =='unknown' else 'visitor')
customerzipcode_stats = customerzipcode_stats[customerzipcode_stats.category == 'es_barsandrestaurants']
customerzipcode_stats["weekday"] = customerzipcode_stats["date"].map(lambda d: (d.weekday()))

#
#  EN CADA ZIPCODE SE CALCULA LA PROPORCIÓN DE CUSTOMERZIPCODE PARA CADA DÍA Y SE HACE UNA ELECCIÓN ALEATORIA SEGÚN LA MISMA
#
def zipify(weekday,zipcode):
    dataf = customerzipcode_df[(customerzipcode_df['weekday'] == weekday) & (customerzipcode_df['merchant_zipcode'] == zipcode)]
    props = dataf.payments_proportion
    tot = props.sum()
    props_items_list = dataf['customerzipcode']
    return np.random.choice(props_items_list, p = list(props / tot))

customerzipcode_stats['customerzipcode_prob'] = customerzipcode_stats.apply(lambda row: zipify(row['weekday'], row['merchant_zipcode']) if row['customerzipcode'] == 'unknown' else row['customerzipcode'],axis=1)


#
#  NOS QUITAMOS LOS ZIPCODES DE VISITANTES
#
customerzipcode_stats = customerzipcode_stats[customerzipcode_stats.customerzipcode != 'visitor']

gbcn = customerzipcode_stats.groupby(["weekday", "customerzipcode_prob", "merchant_zipcode"]).aggregate({ "payments": np.sum })
gbcn = gbcn.reset_index()

total_payments = gbcn.payments.sum()

proba_list = []
customer_list = list(customerzipcode_stats.customerzipcode.unique())
beta = len(customer_list) * len(bcn_zipcodes)
for zipcode in bcn_zipcodes:
    for customer_zipcode in customer_list:
        for weekday in weekday_list:
            proba = {}
            proba["merchant_zipcode"] = zipcode
            proba["customerzipcode"] = customer_zipcode
            proba["weekday"] = weekday
            row = gbcn[(gbcn.weekday == weekday) & (gbcn.customerzipcode_prob == customer_zipcode) & (gbcn.merchant_zipcode == zipcode)]
            if len(row) == 1 :
              payments = int(row.payments)
            else:
              payments = 0
            proba["payments_proportion"] = laplace_correction(payments, total_payments, beta)
            proba_list.append(proba)

db.customerzipcode_aggregation_prob.insert(proba_list)
