# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 12:47:40 2015

@author: daviz
"""

import pandas as pd
import numpy as np
from sklearn import cross_validation

# Load datasets
names = ["merchant_zipcode", "date", "category", "age_interval", "gender", "merchants", "cards", "payments", "avg_payment", "max_payment", "min_payment", "std"]
demo_stats = pd.read_csv("dataset/demographic_distribution000", delim_whitespace=True,
                         names= names, parse_dates=["date"],
                         dtype = {'merchant_zipcode': str})

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
demo_stats["weekday"] = demo_stats["weekday"].astype('string')

demo_stats["amount"] = demo_stats["payments"] * demo_stats["avg_payment"]
demo_stats = demo_stats[demo_stats.amount < 500]
demo_stats = demo_stats[demo_stats.amount > 0]

demo_stats["amount_level"] = pd.cut(demo_stats.amount, 7, labels = ["very-low", "low", "low-medium", "medium", "medium-high", "high", "very-high"])
demo_stats["max_payment_level"] = pd.cut(demo_stats.max_payment, 7, labels = ["very-low", "low", "low-medium", "medium", "medium-high", "high", "very-high"])
demo_stats["min_payment_level"] = pd.cut(demo_stats.min_payment, 7, labels = ["very-low", "low", "low-medium", "medium", "medium-high", "high", "very-high"])

demo_stats = demo_stats.groupby(["weekday","age_interval", "gender",  "max_payment_level", "min_payment_level"])['merchant_zipcode'].apply(list)
demo_stats = demo_stats.reset_index()

demo_stats['merchant_zipcode'] = demo_stats['merchant_zipcode'].map(lambda d: tuple(list(set(d))))

X = demo_stats[["weekday","age_interval", "gender",  "max_payment_level", "min_payment_level"]]
y = demo_stats[["merchant_zipcode"]]



# Allow to use machine learning with categorical features.
from sklearn.feature_extraction import DictVectorizer
vec = DictVectorizer()
X_vectorized = vec.fit_transform(X.to_dict("records")).toarray()

# Multilabel classification
from sklearn.preprocessing import MultiLabelBinarizer
mlb = MultiLabelBinarizer()
y_multilabel = mlb.fit_transform(y.values.ravel())


PRC = 0.2
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X_vectorized, y_multilabel, test_size=PRC)


# OneVsRest
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report

classifier = OneVsRestClassifier(
                SGDClassifier(
                    loss= 'hinge',
                    alpha=0.00001,
                    penalty='l2')).fit(X_train, y_train)

y_predicted= classifier.predict(X_test)
print classification_report(y_test, y_predicted)

# Predict new examples
example = {'age_interval': '35-44',
  'max_payment_level': 'low',
  'min_payment_level': 'low',
  'gender': 'male',
  'weekday': '5'}

example_vectorized = vec.transform(example).toarray()
example_predicted =  classifier.predict(example_vectorized)
print "Person that can not spend lot of money on restaurant:"
print mlb.inverse_transform(example_predicted)
print "\n\n"

example = {'age_interval': '35-44',
  'max_payment_level': 'high',
  'min_payment_level': 'high',
  'gender': 'male',
  'weekday': '5'}
example_vectorized = vec.transform(example).toarray()
example_predicted =  classifier.predict(example_vectorized)
print "Person that can spend more money on restaurant:"
print mlb.inverse_transform(example_predicted)
