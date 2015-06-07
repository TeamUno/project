# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 10:52:15 2015
We are going to analize if people are buying less on transportation on july 2014
We are removing the week seasonal component.
@author: daviz
"""

import pandas as pd
import numpy as np
import seaborn as sns


# Load datasets
names = ["merchant_zipcode", "date", "category", "merchants", "cards", "payments", "avg_payment", "max_payment", "min_payment", "std"]
basic_stats = pd.read_csv("basic_stats000", delim_whitespace=True, names= names, parse_dates=["date"])

# we calculae the avg amount of money.
basic_stats["amount"] = basic_stats["payments"]* basic_stats["avg_payment"]

# ---------------------------------------------------
# Time Series analysis. plot time variation for a category over the week.
categories = basic_stats[basic_stats['category'] == "es_transportation"].pivot_table(values="amount", columns=["category"], index=["date"], aggfunc=np.sum)
categories["date"] = categories.index
categories["weekday"] = categories["date"].map(lambda d: (d.weekday()))
categories["day"] = categories["date"].map(lambda d: d.day)

# Are people buying less on transport?
sns.lmplot("day", "es_transportation", categories)


# To see the trending we should remove the seasonal component over week
def remove_seasonal_component(data, field, target):    
    weekdays = range(0,7)
    total_mean = data[field].mean()
    for weekday in weekdays:
        weekday_index = data['weekday'] == weekday
        weekday_extent =  data.loc[weekday_index, field]
        seasonal_coef = weekday_extent.mean() - total_mean
        data.loc[weekday_index, target] = data.loc[weekday_index, field] - seasonal_coef

remove_seasonal_component(categories, "es_transportation", "without_season")

# it seems that people are buying less over july
sns.lmplot("day", "without_season", categories)
