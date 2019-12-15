from flask import jsonify
from flask_restful import Resource
import redis
import json

MAX_QTY = 10


class Backups(Resource):
    """ Endpoint "/api/v1/backups" implementation """
    def get(self):

        try:
            # Redis DB connection
            redis_db = redis.Redis(host="192.168.10.210", port=6379)

            # Init dict and lists
            response = {}
            sdp_data = []
            oracle_data = []
            buhsrv_data = []
            sudimost_data = []

            # Get last 10 values from redis list
            raw_list = redis_db.lrange("sdp_backup_list", -MAX_QTY, -1)
            for item in raw_list:
                sdp_data.append(json.loads(bytes.decode(item)))

            # Get last 10 values from redis list
            raw_list = redis_db.lrange("oracle_backup_list", -MAX_QTY, -1)
            for item in raw_list:
                oracle_data.append(json.loads(bytes.decode(item)))

            # Get last 10 values from redis list
            raw_list = redis_db.lrange("buhsrv_backup_list", -MAX_QTY, -1)
            for item in raw_list:
                buhsrv_data.append(json.loads(bytes.decode(item)))

            # Get last 10 values from redis list
            raw_list = redis_db.lrange("sudimost_backup_list", -MAX_QTY, -1)
            for item in raw_list:
                sudimost_data.append(json.loads(bytes.decode(item)))

            # Add lists to dict
            response["sdp_backup"] = sdp_data
            response["oracle_backup"] = oracle_data
            response["buhsrv_backup"] = buhsrv_data
            response["sudimost_backup"] = sudimost_data

        except Exception as e:
            # TODO: Add logging
            print(f"RediS DB error: {e}")
            return {"message": "Redis DB Error!"}, 500

        #  Return dict with data as json
        return jsonify(response)
