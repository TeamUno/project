# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 10:43:25 2015

@author: x
"""
import pandas as pd



def importdata():
    folder = "../dataset/"
    names=['zipcode','date','category','merchant','card', 'payment', 'avg', 'max', 'min', 'std']
    basic_stats = pd.io.parsers.read_table(folder + 'basic_stats000',sep='\t', names=names, parse_dates=["date"])
    basic_stats=improvedata()
    return basic_stats

def improvedata():
    basic_stats["amount"] = basic_stats["payment"]* basic_stats["avg"]
    basic_stats["avgpaybymerch"] = basic_stats["payment"]/basic_stats["merchant"]
    basic_stats["amountbymerch"] = basic_stats["amount"]/basic_stats["merchant"]
    basic_stats["avgReppays"] = basic_stats["payment"]/basic_stats["card"]
    basic_stats["weekday"] = basic_stats["date"].map(lambda d: (d.weekday()))
    basic_stats["day"] = basic_stats["date"].map(lambda d: ('{0:%d}-{0:%a}'.format(d)))
    return basic_stats
    
if __name__ == '__main__':
    global  basic_stats
    basic_stats=None
    
