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
               "55-65": range(55, 65),
               ">65":   range(65, 100) }

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")


class PlacesHandler(web.RequestHandler):
    def post(self):
        preference_data = {}
        gender = ""
        age_interval = ""
        if self.request.body != "":
            preference_data = json.loads(self.request.body)
        if preference_data["gender"] != '':
            gender = preference_data["gender"]
        if preference_data["age"] != '':
            for key, ranges in age_ranges.iteritems():
                if int(preference_data["age"]) in ranges:
                   age_interval = key

        weekday = str(datetime.date.today().weekday())

        zipcode_aggregation = db.merchant_zipcode_aggregation.find({ "age_interval": age_interval,
                                                          "gender": gender,
                                                          "weekday": weekday }).sort("payments_proportion", pymongo.DESCENDING)

        geo_json = db.merchant_zipcode_coordinates.find().next()
        for aggregation in zipcode_aggregation:
            index = next(index  for (index, feature) in enumerate(geo_json['features']) if feature['properties']['zipcode'] == aggregation['merchant_zipcode'])
            geo_json['features'][index]["properties"]["payments_proportion"] = aggregation['payments_proportion']


        #TODO writing to a file? FIX. json.dump not working with geo_json.
        #with open("merchant_zipcode.geo_json", "w") as fp:
        #    json.dump(geo_json, fp)

        #TODO sending geo_json via request? FIX. json.dumps not working with geo_json
        #self.set_header("Content-Type", "application/json")
        #self.write(json.dumps(geo_json), default=json_util.default))


class PlaceHandler(web.RequestHandler):
    def get(self, place_id):
        place = db.places.find_one({"_id": ObjectId(str(place_id))})
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(place, default=json_util.default))


settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": True
}

application = web.Application([
    (r'/', IndexHandler),
    (r'/index', IndexHandler),
    (r'/api/v1/places', PlacesHandler),
    (r'/api/v1/places/(.*)', PlaceHandler)
], **settings)

if __name__ == "__main__":
    application.listen(3333)
    ioloop.IOLoop.instance().start()
