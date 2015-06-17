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
demo_stats = pd.read_csv("dataset/demographic_distribution000", delim_whitespace=True, names= names, parse_dates=["date"])


demo_stats = demo_stats.loc[demo_stats["gender"] != 'unknown']
demo_stats = demo_stats.loc[demo_stats["age_interval"] != 'unknown']

demo_stats["amount"] = demo_stats["payments"] * demo_stats["avg_payment"]
demo_stats = demo_stats[["merchant_zipcode", "date", "category", "age_interval", "gender", "merchants", "cards", "payments", "amount"]]

# Aggregation by age_interval and categories
gbcn = pd.pivot_table(demo_stats, values = "amount", index=["age_interval", "gender"], columns=["category"],
                      aggfunc=np.sum, fill_value=0 )

# ---------------------------------------------------------------------
# We can cluster similar age and gender behaviours throgh categories.

age_intervals = gbcn.index
categories = gbcn.columns
n_clusters = 4
print gbcn.shape
kmeans = cluster.KMeans(init='k-means++',n_clusters= n_clusters)
y_pred = kmeans.fit_predict(gbcn.values)
for n in range(n_clusters):
    print "Cluster "+ str(n) + ": " + str([gbcn.index[i] for i, item in enumerate(y_pred) if item == n ])
