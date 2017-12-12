from flask import Flask, jsonify, request, redirect, url_for
from flask_restful import reqparse, abort, Api, Resource
from flask_pymongo import PyMongo
import time

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "iot_db"
app.config["MONGO_HOST"] = "mongo.iot.svc.cluster.local"
mongo = PyMongo(app, config_prefix='MONGO')
api = Api(app)


class Device(Resource):
    def get(self, device_id):
        device = mongo.db.devices.find_one({"_id": device_id})
        if device:
            #del device["_id"]
            return jsonify(device)        
        else:
            abort(404, message="Device {} doesn't exist".format(device_id))

    def put(self, device_id):
        data = request.get_json()
        mongo.db.devices.update({'_id': device_id}, {'$set': data})
        return ('', 204)

    def delete(self, device_id):
        mongo.db.devices.remove({'_id': device_id})
        return ('', 204)



class DeviceList(Resource):
    def get(self):
        device_list = []
        cursor = mongo.db.devices.find({})
        for device in cursor:
            del device["measures"]
            device_list.append(device)
        return jsonify(device_list)

    def post(self):
        data = request.get_json()
        mongo.db.devices.insert(data)
        return ('', 201)

class Measure(Resource):
    def post(self):
        data = request.get_json()
        store = {'time': time.ctime(), 'value': data["value"]}
        try:
            device = {'_id': data["device_id"], 'type': data["type"], "measurable_var": "generic"}
            mongo.db.devices.insert(device)
        except:
            print("document already exists")
        mongo.db.devices.update({'_id': data["device_id"]}, {'$addToSet': {'measures': store}})
        mongo.db.devices.update({'_id': data["device_id"]}, {'$addToSet': {'measures': store}})
        print(data["device_id"])
        return ('', 201)


api.add_resource(DeviceList, '/devices')
api.add_resource(Measure, '/measure')
api.add_resource(Device, '/device/<string:device_id>')


if __name__ == '__main__':
    app.run(host="0.0.0.0")