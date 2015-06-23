import os
from tornado import ioloop,web
from tornado.escape import json_encode
from pymongo import MongoClient
import json
from bson import json_util
from bson.objectid import ObjectId


MONGODB_DB_URL = os.environ.get('OPENSHIFT_MONGODB_DB_URL') if os.environ.get('OPENSHIFT_MONGODB_DB_URL') else 'mongodb://localhost:27017/'
MONGODB_DB_NAME = os.environ.get('OPENSHIFT_APP_NAME') if os.environ.get('OPENSHIFT_APP_NAME') else 'wherelocalsgo'

client = MongoClient(MONGODB_DB_URL)
db = client[MONGODB_DB_NAME]


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")


class PlacesHandler(web.RequestHandler):
    def post(self):
        preference_data = {}
        if self.request.body != "":
            preference_data = json.loads(self.request.body)
        cp = db.demographic_distribution.find({'gender': preference_data["gender"], 'category': preference_data["category"]}).count()
        places = db.places.find({})[:3]
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(list(places), default=json_util.default))


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
