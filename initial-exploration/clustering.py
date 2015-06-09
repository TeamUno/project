# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 12:41:11 2015

@author: daviz
"""

# using clustering as a exploratory analysis.
# Adding new attributes to the dataset using a dummy clusterization

from  sklearn import cluster
import sklearn.preprocessing
from sklearn.feature_extraction import DictVectorizer
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('ggplot')

# Load datasets
names = ["merchant_zipcode", "date", "category", "merchants", "cards", "payments", "avg_payment", "max_payment", "min_payment", "std"]
basic_stats = pd.read_csv("basic_stats000", delim_whitespace=True, names= names, parse_dates=["date"])
basic_stats["amount"] = basic_stats["payments"] * basic_stats["avg_payment"]
bcn = basic_stats[basic_stats["merchant_zipcode"] < 8044]

# Aggregation by merchant_zipcode
gbcn = bcn.groupby("merchant_zipcode").sum()
gbcn["merchant_zipcode"] = gbcn.index

# -----------------------------------------------------------------

def plot_cluster():
    plt.scatter(gbcn.loc[y_pred == 0, "merchant_zipcode"], gbcn.loc[y_pred == 0, "amount"], c="b")
    plt.scatter(gbcn.loc[y_pred == 1, "merchant_zipcode"], gbcn.loc[y_pred == 1, "amount"], c="r")
    plt.scatter(gbcn.loc[y_pred == 2, "merchant_zipcode"], gbcn.loc[y_pred == 2, "amount"], c="g")
    plt.scatter(gbcn.loc[y_pred == 3, "merchant_zipcode"], gbcn.loc[y_pred == 3, "amount"], c="y")
   

# ---------------------------------------------------------------------
# kmeans clustering
kmeans = cluster.KMeans(init='k-means++',n_clusters=4)
kmeans.fit(gbcn[["merchant_zipcode", "amount"]])

y_pred = kmeans.labels_.astype(np.int)

centroids = kmeans.cluster_centers_
plt.subplot(2,2,1)
plt.scatter(centroids[:, 0], centroids[:, 1],
            marker='x', s=169, linewidths=3,
            color='w', zorder=10)
            
plot_cluster()

# we can use this cluster to add attributes to the dataset
level_amount = {0: 'low', 1: 'low-medium', 2: 'medium', 3: 'high', }

def select_level_amount(row):
    cluster = kmeans.predict(row[["merchant_zipcode", "amount"]])
    return level_amount[cluster[0]]
    
gbcn["level_amount"] = gbcn.apply(select_level_amount, axis=1)         

# --------------------------------------------------------------------
# Spectral clustering
spectral = cluster.SpectralClustering(n_clusters=4, affinity="cosine")
spectral.fit(gbcn[["merchant_zipcode", "amount"]])
y_pred = spectral.labels_.astype(np.int)

plt.subplot(2,2,2)

plot_cluster()

# ---------------------------------------------------------------------------
# hierarchical clustering
agglomerative = cluster.AgglomerativeClustering(n_clusters=4,
                                                affinity="manhattan",
                                                linkage="average")
y_pred = agglomerative.fit_predict(gbcn[["merchant_zipcode", "amount"]])

plt.subplot(2,2,3)

plot_cluster()

