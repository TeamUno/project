# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 19:53:18 2015

@author: daviz
"""

import pandas as pd
import numpy as np

# Load datasets
names = ["merchant_zipcode", "date", "category", "merchants", "cards", "payments", "avg_payment", "max_payment", "min_payment", "std"]
basic_stats = pd.read_csv("basic_stats000", delim_whitespace=True, names= names, parse_dates=["date"])

names = ["merchant_zipcode", "date", "category", "client_zipcode", "merchants", "cards", "payments", "avg_payment", "max_payment", "min_payment", "std"]
customer_zipcodes = pd.read_csv("customer_zipcodes000", delim_whitespace=True, names=names, parse_dates=["date"])

names = ["merchant_zipcode", "date", "category", "age_interval", "merchants", "cards", "payments", "avg_payment", "max_payment", "min_payment", "std"]
age_distribution = pd.read_csv("age_distribution000", delim_whitespace=True, names=names, parse_dates=["date"])

names = ["merchant_zipcode", "date", "category", "gender", "merchants", "cards", "payments", "avg_payment", "max_payment", "min_payment", "std"]
gender_distribution = pd.read_csv("gender_distribution000", delim_whitespace=True, names=names, parse_dates=["date"])

names = ["merchant_zipcode", "date", "category", "payment_interval", "merchants", "cards", "payments", "avg_payment", "max_payment", "min_payment", "std"]
payment_distribution = pd.read_csv("payment_distribution000", delim_whitespace=True, names=names, parse_dates=["date"])

names = ["merchant_zipcode", "date", "category", "age_interval", "gender", "merchants", "cards", "payments", "avg_payment", "max_payment", "min_payment", "std"]
demographic_distribution = pd.read_csv("demographic_distribution000", delim_whitespace=True, names=names, parse_dates=["date"])

names = ["merchant_zipcode", "date", "day_of_week", "hour",  "merchants", "cards", "payments", "avg_payment", "max_payment", "min_payment", "std"]
expenditure_time_curve = pd.read_csv("expenditure-time_curve000", delim_whitespace=True, names=names, parse_dates=["date"])

#--------------------------------------------------------------
# Which days people pay more on transportation?

dayOfWeek={0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
basic_stats["dayname"] = basic_stats["date"].apply(lambda l: dayOfWeek[l.weekday()])
transportation = basic_stats[basic_stats['category'] == "es_transportation"].pivot_table(values="payments", columns=["category"], index=["dayname"], aggfunc=np.sum)
transportation.sort("es_transportation", inplace=True, ascending=False)
transportation.plot(kind="bar")

# -------------------------------------
# Who spend more money on health Men or Women?. Agregation by gender: merging 2 datasets. 

data = pd.merge(basic_stats, gender_distribution, on=["merchant_zipcode", "date", "category"])

health = data[data['category'] == "es_health"].pivot_table(values="payments_x", columns=["category"], index=["gender"], aggfunc=np.sum)
health.plot(kind="bar")
# There is a lot of unknown gender. Be careful!


#----------------------------------------------
# demographic initial study. where and how much the different social layer are buying on bcn.

demo = demographic_distribution
demo = demo.loc[demo["gender"] != 'unknown']
demo = demo.loc[demo["age_interval"] != 'unknown']
# Calculate the avg amount
demo["amount"] = demo["payments"]* demo["avg_payment"]
# Focus on BCN zipcodes.
demo = demo.loc[demo.merchant_zipcode < 8042]
# For now let's remove outliers to have a better scatterplot.
demo =  demo[demo["amount"] < 500]

s = demo.pivot_table(values="amount", index="merchant_zipcode", columns=["age_interval"])
s["x"] = s.index

ax = s.plot(kind="scatter", x= "x",y = "45-54", color="Red", label="45-54" )
bx = s.plot(kind="scatter", x= "x",y = "35-44", color="Blue", label="35-44", ax = ax)
s.plot(kind="scatter", x= "x",y = "25-34", color="Green", label="amount", ax= bx)

