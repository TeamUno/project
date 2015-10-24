# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 15:23:29 2015

@author: daviz
"""

import foursquare as fq
#import json
import csv
import os
import pandas as pd

# Construct the client object
os.environ.get('FOURSQUARE_CLIENT_ID')
client = fq.Foursquare(client_id = os.environ.get('FOURSQUARE_CLIENT_ID'),
                       client_secret = os.environ.get('FOURSQUARE_CLIENT_SECRET'))

bcn_zipcodes = ['08001', '08002', '08003', '08004', '08005', '08006', '08007',
                '08008', '08009', '08010', '08011', '08012', '08013', '08014',
                '08015', '08016', '08017', '08018', '08019', '08020', '08021',
                '08022', '08023', '08024', '08025', '08026', '08027', '08028',
                '08029', '08030', '08031', '08032', '08033', '08034', '08035',
                '08036', '08037', '08038', '08039', '08040', '08041', '08042']

# print json.dumps(response['groups'] ,indent=2, separators=(',', ': '))

with open('dataset/top_venues.csv', 'w') as csvfile:
    fieldnames = ['name', 'rating', 'price', 'phone', 'city', 'merchant_zipcode',
                  'address', 'latitude', 'longitude', 'category']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for zipcode in bcn_zipcodes:
        response = client.venues.explore(params= {'near': zipcode + ", Barcelona, Cataluña", 'limit': 50})
        for groups in response['groups']:
            for group in groups['items']:
                venue = group['venue']
                venue_row = { 'name': None, 'rating': None, 'price': None, 'phone': None,
                          'city': None, 'merchant_zipcode': None, 'address': None,
                          'latitude': None, 'longitude': None, 'category': None }
                venue_row['name'] = venue['name']
                if 'rating' in venue:
                    venue_row['rating'] = venue['rating']
                if 'price' in venue:
                     #1 is < $10 an entree, 2 is $10-$20 an entree, 3 is $20-$30 an entree, 4 is > $30
                    venue_row['price'] = venue['price']['tier']
                if 'phone' in venue['contact']:
                    venue_row['phone']= venue['contact']['phone']
                if 'city' in venue['location']:
                    venue_row['city'] = venue['location']['city']
                if 'postalCode' in venue['location']:
                    venue_row['merchant_zipcode'] = venue['location']['postalCode']
                if 'address' in venue['location']:
                    venue_row['address'] = venue['location']['address']
                if 'lat' in venue['location']:
                    venue_row['latitude'] = venue['location']['lat']
                if 'lng' in venue['location']:
                    venue_row['longitude'] = venue['location']['lng']
                for categories in venue['categories']:
                    category_list = []
                    if 'name' in categories:
                        category_list.append(categories['name'])
                    venue_row['category'] = ",".join(category_list)

                writer.writerow(venue_row)
top_venues = pd.read_csv("dataset/top_venues.csv")
top_venues.drop_duplicates(inplace=True)
top_venues.to_csv("dataset/top_venues.csv")
