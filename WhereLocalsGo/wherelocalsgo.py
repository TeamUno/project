import os
from tornado import ioloop,web
from tornado.escape import json_encode
import pymongo
import json
from bson import json_util
from bson.objectid import ObjectId
import datetime


MONGODB_DB_URL = os.environ.get('OPENSHIFT_MONGODB_DB_URL') if os.environ.get('OPENSHIFT_MONGODB_DB_URL') else 'mongodb://localhost:27017/'
MONGODB_DB_NAME = os.environ.get('OPENSHIFT_APP_NAME') if os.environ.get('OPENSHIFT_APP_NAME') else 'wherelocalsgo'

client = pymongo.MongoClient(MONGODB_DB_URL)
db = client[MONGODB_DB_NAME]

age_ranges = { "<25":   range(0, 25),
               "25-34": range(25, 35),
               "35-44": range(35, 45),
               "45-54": range(45, 55),
               "55-64": range(55, 65),
               ">=65":  range(65, 100) }
bcn_zipcodes = ['08001', '08002', '08003', '08004', '08005', '08006', '08007',
                '08008', '08009', '08010', '08011', '08012', '08013', '08014',
                '08015', '08016', '08017', '08018', '08019', '08020', '08021',
                '08022', '08023', '08024', '08025', '08026', '08027', '08028',
                '08029', '08030', '08031', '08032', '08033', '08034', '08035',
                '08036', '08037', '08038', '08039', '08040', '08041', '08042']


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")


class PlacesHandler(web.RequestHandler):
    def post(self):
        preference_data = {}
        if self.request.body != "":
            preference_data = json.loads(self.request.body)

        if preference_data["zipcode"] != '':
            query = {'zipcode': preference_data["zipcode"]}

        places = db.places.find(query)
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(list(places), default=json_util.default))


class PlaceHandler(web.RequestHandler):
    def get(self, place_id):
        place = db.places.find_one({"_id": ObjectId(str(place_id))})
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(place, default=json_util.default))


class MapsHandler(web.RequestHandler):
    def post(self):
        preference_data = {}
        gender = ""
        age_interval = ""
        customerzipcode = ""

        if self.request.body != "":
            preference_data = json.loads(self.request.body)
        if preference_data["gender"] != '':
            gender = preference_data["gender"]
        if preference_data["customerzipcode"] != '':
            customerzipcode = preference_data["customerzipcode"]
        if preference_data["age"] != '':
            for key, ranges in age_ranges.iteritems():
                if int(preference_data["age"]) in ranges:
                   age_interval = key
        if preference_data["weekday"] != '':
            # range changed to adapted to python weekday
            weekday = int(preference_data["weekday"])
            weekday= weekday -1 if weekday != 0 else 6
        else:
            weekday = datetime.date.today().weekday()

# TODO remove?
#        if preference_data["gender"] != '':
#            query={ "age_interval": age_interval,
#                          "gender": gender,
#                          "weekday": weekday }
# #           order =pymongo.DESCENDING
#        else:
#            query={ "age_interval": age_interval,
#                          "weekday": weekday }
##            order = pymongo.ASCENDING
#        zipcode_aggregation = db.merchant_zipcode_aggregation.find(query).sort("payments_proportion", order)

        # We calculate probability where a user will go to a merchant_zipcode based on the preferences using
        # Naive Bayes calculations.
        zipcode_proba = naive_bayes_probabilities(age_interval, gender, weekday, customerzipcode)

        # We normalize values relative to the max probability found, so we can have a scale from 0-1 where 1 is
        # the max probability and the following values will be proportion from the max value.
        zipcode_proba = normalize_relative_to_max(zipcode_proba)

        #interpolate probabilities inside the geo_json properties so the map can find this normalize value for every zipcode
        geo_json = interpolate_proba_to_geojson_zipcodes(zipcode_proba)

        self.set_header("Content-Type", "application/json")
        self.write(geo_json)


def naive_bayes_probabilities(age_interval, gender, weekday, customerzipcode):
    zipcode_proba = {}
    for zipcode in bcn_zipcodes:

        ageinterval_proba = db.ageinterval_aggregation.find_one( {"ageinterval": age_interval, "merchant_zipcode": zipcode})["payments_proportion"]

        if gender != "":
            gender_proba = db.gender_aggregation.find_one( {"gender": gender, "merchant_zipcode": zipcode})["payments_proportion"]
        else:
            gender_proba = 1

        weekday_proba = db.weekday_aggregation.find_one( {"weekday": weekday, "merchant_zipcode": zipcode})["payments_proportion"]

        if customerzipcode != "":
            customer_proba = db.customerzipcode_aggregation.find_one( {"customerzipcode": customerzipcode, "merchant_zipcode": zipcode})["payments_proportion"]
        else:
            customer_proba = 1

        # Naive Bayes probability.
        zipcode_proba[zipcode] =  ageinterval_proba * weekday_proba
    return zipcode_proba

def normalize_relative_to_max(zipcode_proba):
    max_proba = max(zipcode_proba.values())
    for zipcode in zipcode_proba:
        zipcode_proba[zipcode] = zipcode_proba[zipcode] / max_proba
    return zipcode_proba

def interpolate_proba_to_geojson_zipcodes(zipcode_proba):
    geo_json = db.merchant_zipcode_coordinates.find({}, {"_id": 0}).next()
    for zipcode in bcn_zipcodes:
        index = next(index  for (index, feature) in enumerate(geo_json['features']) if feature['properties']['zipcode'] == zipcode)
        geo_json['features'][index]["properties"]["payments_proportion"] = zipcode_proba[zipcode]
    return geo_json

settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": True
}

application = web.Application([
    (r'/', IndexHandler),
    (r'/index', IndexHandler),
    (r'/api/v1/places', PlacesHandler),
    (r'/api/v1/places/(.*)', PlaceHandler),
    (r'/api/v1/maps', MapsHandler)
], **settings)

if __name__ == "__main__":
    application.listen(3333)
    ioloop.IOLoop.instance().start()
