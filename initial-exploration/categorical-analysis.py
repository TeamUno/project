# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 20:01:36 2015
@author: daviz

Numerical and Categorical variable Analysis 

"""
import pandas as pd
import matplotlib  as plt
plt.style.use('ggplot')



names = ["merchant_zipcode", "date", "category", "age_interval", "gender",
         "merchants", "cards", "payments", "avg_payment", "max_payment",
         "min_payment", "std"]
demo_distr = pd.read_csv("demographic_distribution000", delim_whitespace=True,
                         names=names, parse_dates=["date"])


# Show types of variables 
print demo_distr.ftypes
"""
merchant_zipcode             int64:dense
date                datetime64[ns]:dense
category                    object:dense
age_interval                object:dense
gender                      object:dense
merchants                    int64:dense
cards                        int64:dense
payments                     int64:dense
avg_payment                float64:dense
max_payment                float64:dense
min_payment                float64:dense
std                        float64:dense

It seems we have 3 categorical variables: category, age_interval, gender. 
Date is datetime as we specified before on read_csv
and the rest are numerical.

"""

# Fast view of the data
print demo_distr.head(5)

# Describe it is only for numerical variables
print demo_distr.describe()
"""
       merchant_zipcode     merchants         cards      payments
count      48538.000000  48538.000000  48538.000000  48538.000000   
mean       10760.598418      8.500268     52.836726     56.120813   
std         7656.320109      5.582593    134.288949    149.437862   
min         8001.000000      5.000000      3.000000      5.000000   
25%         8021.000000      5.000000      6.000000      7.000000   
50%         8211.000000      6.000000     15.000000     16.000000   
75%         8800.000000      9.000000     55.000000     59.000000   
max        43892.000000     71.000000   6454.000000   7792.000000 

std of cards and payments are very relevant. A lot of dispersion.


"""
#removing unknown values
print demo_distr.age_interval.unique()
demo_distr = demo_distr.loc[demo_distr["age_interval"]  != "unknown"]
print demo_distr.gender.unique()
demo_distr = demo_distr.loc[demo_distr["gender"]  != "unknown"]

# removing outliers, although we should see if they are outlier or not.
# but for now we remove it to have better analysis
def remove_outlier(data, field):
    outlier = data[field].mean() + 3*data[field].std()
    data = data.loc[data[field] < outlier ]

remove_outlier(demo_distr, "merchants")
remove_outlier(demo_distr, "cards")
remove_outlier(demo_distr, "payments")


# ---------------------------------------------------------
# Numerical variables analysis

# we can see from the boxplot that the historgram is skewed
demo_distr.merchants.plot(kind="box")

# we have a positive skewed histogram
demo_distr.merchants.plot(kind="hist")


# We can create boxplot that combines numerical and categorical variables
demo_distr.boxplot(column="payments", by="age_interval")
demo_distr.boxplot(column="payments", by="gender")

# Categorical variable Analysis

# see different values of the categorical variable
print demo_distr.gender.unique()

demo_distr["gender"] = pd.Categorical(demo_distr.gender)
demo_distr["category"] = pd.Categorical(demo_distr.category)
demo_distr["age_interval"] = pd.Categorical(demo_distr.age_interval)

# as categorical variable we can count per categories
print demo_distr.category.value_counts()

# cross tabulation of age_interval and gender.
cross_tab = pd.crosstab(demo_distr.age_interval, demo_distr.gender)
cross_tab.plot(kind='bar', stacked=True, grid=False)