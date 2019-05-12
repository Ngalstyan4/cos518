from flask import Flask
from flask_restful import Api, Resource, reqparse

from hyperbolic import HyperbolicCache
app = Flask(__name__)
api = Api(app)
print("haha")
cache = HyperbolicCache(5,3)
# for i in range(100):
#     self.cache.put(i, 0, 0)
#     self.cache.put(1000, 0, 0)
#     #self.cache.print_cache()

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

app.run(host='0.0.0.0', port=3000, debug=True)
