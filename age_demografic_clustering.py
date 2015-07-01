# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 12:41:11 2015

@author: daviz
"""

# using clustering as a exploratory analysis.
# Adding new attributes to the dataset using a dummy clusterization

from  sklearn import cluster
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('ggplot')

# Load datasets
names = ["merchant_zipcode", "date", "category", "age_interval", "gender", "merchants", "cards", "payments", "avg_payment", "max_payment", "min_payment", "std"]
demo_stats = pd.read_csv("dataset/demographic_distribution000", delim_whitespace=True, names= names, parse_dates=["date"], dtype = {'merchant_zipcode': str})


demo_stats = demo_stats.loc[demo_stats["gender"] != 'unknown']
demo_stats = demo_stats.loc[demo_stats["age_interval"] != 'unknown']
demo_stats = demo_stats[demo_stats.category == 'es_barsandrestaurants']

bcn_zipcodes = ['08001', '08002', '08003', '08004', '08005', '08006', '08007',
                '08008', '08009', '08010', '08011', '08012', '08013', '08014',
                '08015', '08016', '08017', '08018', '08019', '08020', '08021',
                '08022', '08023', '08024', '08025', '08026', '08027', '08028',
                '08029', '08030', '08031', '08032', '08033', '08034', '08035',
                '08036', '08037', '08038', '08039', '08040', '08041', '08042']

demo_stats = demo_stats[demo_stats.merchant_zipcode.apply(lambda zp: zp in bcn_zipcodes)]

demo_stats["weekday"] = demo_stats["date"].map(lambda d: (d.weekday()))
#let see only weekend
demo_stats = demo_stats[demo_stats.weekday.isin([5,6])]
demo_stats["weekday"] = demo_stats["weekday"].astype('string')


demo_stats["amount"] = demo_stats["payments"] * demo_stats["avg_payment"]
demo_stats["max_payment_level"] = pd.cut(demo_stats.max_payment, 7, labels = ["very-low", "low", "low-medium", "medium", "medium-high", "high", "very-high"])
demo_stats["min_payment_level"] = pd.cut(demo_stats.min_payment, 7, labels = ["very-low", "low", "low-medium", "medium", "medium-high", "high", "very-high"])

#TODO calculate the mean for max_payment and min_payment when we aggregate by "age_interval", "gender", "weekday", "merchant_zipcode" and
# introduce it on the clustering

demo_stats = demo_stats[["merchant_zipcode", "category", "weekday", "age_interval", "gender", "amount", "max_payment_level", "min_payment_level"]]

# Aggregation by age_interval and
gbcn = pd.pivot_table(demo_stats, values = "amount", index=["age_interval", "gender", "weekday", "merchant_zipcode"], columns=["category"],
                      aggfunc=np.sum, fill_value=0 )

gbcn_reset = gbcn.reset_index()
from sklearn.feature_extraction import DictVectorizer
categorical = gbcn_reset[["age_interval", "gender", "merchant_zipcode", "weekday"]]
vec = DictVectorizer()
categorical_features = vec.fit_transform(categorical.to_dict("records"))

from scipy.sparse import hstack
numerical_features = gbcn_reset[['es_barsandrestaurants']]
X = hstack([categorical_features, numerical_features])


# ---------------------------------------------------------------------
# We can cluster similar age and gender behaviours through categories.

n_clusters = 10


kmeans = cluster.KMeans(init='k-means++',n_clusters= n_clusters)
y_pred = kmeans.fit_predict(X)
for n in range(n_clusters):
    print "Cluster "+ str(n) + ":\n " + str([categorical.loc[i].to_dict() for i, item in enumerate(y_pred) if item == n ]) + "\n"


