from flask import Flask
from flask_restful import Api, Resource, reqparse

from hyperbolic import HyperbolicCache
from lru_cache import LRUCache

app = Flask(__name__)
api = Api(app)
print("haha")

cache_size = 1000
cache = HyperbolicCache(cache_size, 64)
#cache = LRUCache(cache_size)

class Cache(Resource):
    def __init__(self):
        self.cache = cache        

    def get(self, key):
        return self.cache.get(int(key)), 200

    def post(self, key):
        return "use put instead", 403

    def put(self, key):
        parser = reqparse.RequestParser()
        parser.add_argument("value")
        parser.add_argument("cost")
        args = parser.parse_args()

        if args["cost"] is None:
            args["cost"] = 0;
        else:
            try:
                args["cost"] = int(args["cost"])
            except:
                args["cost"] = 0;
                print("Warning: non-integer cost ignored")

        self.cache.put(int(key), args["value"], args["cost"])
        return "key:{} value:{} cost:{}".format(key,args["value"],args["cost"]), 200
      
api.add_resource(Cache, "/<int:key>")

import logging
logging.basicConfig(filename='error.log',level=logging.DEBUG)
    
app.run(host='0.0.0.0', port=3000, debug=False)
