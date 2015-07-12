# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 02:32:28 2015

@author: diego based on @davidz
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

db.drop_collection("gender_aggregation")
db.drop_collection("gender_aggregation_prob")

names = ["merchant_zipcode", "date", "category", "gender", "merchants", "cards", "payments", "avg_payments", "max_payments", "min_payments", "std"]
gender_stats = pd.read_csv("../dataset/gender_distribution000",  delim_whitespace=True, names= names, parse_dates=["date"], dtype = {'merchant_zipcode': str})

bcn_zipcodes = ['08001', '08002', '08003', '08004', '08005', '08006', '08007',
                '08008', '08009', '08010', '08011', '08012', '08013', '08014',
                '08015', '08016', '08017', '08018', '08019', '08020', '08021',
                '08022', '08023', '08024', '08025', '08026', '08027', '08028',
                '08029', '08030', '08031', '08032', '08033', '08034', '08035',
                '08036', '08037', '08038', '08039', '08040', '08041', '08042']

gender_list = ["male", "female", "enterprise"]
weekday_list = range(0,7)


gender_stats = gender_stats[gender_stats.merchant_zipcode.apply(lambda zp: zp in bcn_zipcodes)]
gender_stats = gender_stats[gender_stats.gender != 'unknown']
gender_stats = gender_stats[gender_stats.category == 'es_barsandrestaurants']
gender_stats["weekday"] = gender_stats["date"].map(lambda d: (d.weekday()))

#
#  EN CADA ZIPCODE SE CALCULA LA PROPORCIÓN DE MALE, FEMALE Y ENTERPRISE Y SE HACE LA CORRECCIÓN DE LAPLACE POR SI NO HAY NINGUNO
#

def laplace_correction(payments, total_payments, beta):
    return ( payments + 1. ) / (total_payments + beta)

gbcn = gender_stats.groupby(["gender", "weekday", "merchant_zipcode"]).aggregate({ "payments": np.sum })
gbcn = gbcn.reset_index()
total_payments = gbcn.payments.sum()
proba_list = []
beta = len(bcn_zipcodes) * len(gender_list) * len(weekday_list)
for zipcode in bcn_zipcodes:
    for gender in gender_list:
        for weekday in weekday_list:
            proba = {}
            proba["merchant_zipcode"] = zipcode
            proba["gender"] = gender
            proba["weekday"] = weekday
            row = gbcn[(gbcn.weekday == weekday) & (gbcn.gender == gender) & (gbcn.merchant_zipcode == zipcode)]
            if len(row) == 1 :
              payments = int(row.payments)
            else:
              payments = 0
            proba["payments_proportion"] = laplace_correction(payments,total_payments, beta)
            proba_list.append(proba)
        
db.gender_aggregation.insert(proba_list)

gender_df=pd.DataFrame(proba_list)

gender_stats = pd.read_csv("../dataset/gender_distribution000",  delim_whitespace=True, names= names, parse_dates=["date"], dtype = {'merchant_zipcode': str})
gender_stats = gender_stats[gender_stats.merchant_zipcode.apply(lambda zp: zp in bcn_zipcodes)]
gender_stats = gender_stats[gender_stats.category == 'es_barsandrestaurants']
gender_stats["weekday"] = gender_stats["date"].map(lambda d: (d.weekday()))
#
#  EN CADA ZIPCODE SE CALCULA LA PROPORCIÓN DE MALE, FEMALE Y ENTERPRISE PARA CADA DÍA Y SE HACE UNA ELECCIÓN ALEATORIA SEGÚN LA MISMA
#
def genderify(weekday,zipcode):
    dataf = gender_df[(gender_df['weekday'] == weekday) & (gender_df['merchant_zipcode'] == zipcode)]
    props = dataf.payments_proportion
    tot = props.sum()
    props_items_list = dataf['gender']
    return np.random.choice(props_items_list, p = list(props / tot))

gender_stats['gender_prob']=gender_stats.apply(lambda row: genderify(row['weekday'], row['merchant_zipcode']) if row['gender'] == 'unknown' else row['gender'],axis=1)

#
#  ÚLTIMO PASO, PARA VOLVER A CALCULAR P(GENDE||ZIPCODE,WEEKDAY), AHORA CON LOS DATOS DE POBLACIÓN GENERADA + REAL, SÓLO DE MALE Y FEMALE
#
gender_list = ["male", "female"]
gender_stats = gender_stats[gender_stats.gender != 'enterprise']


gbcn = gender_stats.groupby(["weekday", "gender_prob", "merchant_zipcode"]).aggregate({ "payments": np.sum })
gbcn = gbcn.reset_index()
total_payments = gbcn.payments.sum()
proba_list = []
beta = len(bcn_zipcodes) * len(gender_list) * len(weekday_list)
for zipcode in bcn_zipcodes:
    for gender in gender_list:
        for weekday in weekday_list:
            proba = {}
            proba["merchant_zipcode"] = zipcode
            proba["gender"] = gender
            proba["weekday"] = weekday
            row = gbcn[(gbcn.weekday == weekday) & (gbcn.gender_prob == gender) & (gbcn.merchant_zipcode == zipcode)]
            if len(row) == 1 :
              payments = int(row.payments)
            else:
              payments = 0
            proba["payments_proportion"] = laplace_correction(payments,total_payments, beta)
            proba_list.append(proba)

db.gender_aggregation_prob.insert(proba_list)
