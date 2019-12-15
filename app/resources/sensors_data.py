from flask import jsonify
from flask_restful import Resource

import mysql.connector
from mysql.connector import errorcode

import os

import logging
# import app.log.log_config
import log.log_config

MAX_SENSOR_NUM = 3  # sensors id will be 1, 2, 3

MYSQL_ITSM18_USER = os.environ.get("MYSQL_ITSM18_USER") or "SOME_USER"
MYSQL_ITSM18_PASS = os.environ.get("MYSQL_ITSM18_PASS") or "SOME_PASS"

mysql_config = {
  'user': MYSQL_ITSM18_USER,
  'password': MYSQL_ITSM18_PASS,
  'host': '192.168.10.210',
  'database': 'log_data_db',
  'ssl_disabled': 'True'
}

# retrieve logger
sns_logger = logging.getLogger("sensor_log")

class Sensors(Resource):

    def get(self, sensor_id):
        sensor_data_list = []
        conn = None
        cur = None

        # check sensor_id
        if sensor_id > MAX_SENSOR_NUM:
            sid = 1
        else:
            sid = sensor_id

        sns_logger.debug(f"SensorID={sid}")

        # connect to mysql and get data
        try:
            conn = mysql.connector.connect(**mysql_config)
            cur = conn.cursor()
            query = "select (sensors_log.timestamp_utc + INTERVAL 3 HOUR) as datetime_local, \
                    sensors_log.sensor_value_string from sensors_log \
                    where sensors_log.timestamp_utc > (NOW() - INTERVAL 24 HOUR) \
                    and sensors_log.sensor_id='{}'".format(sid)
            cur.execute(query)

            # copy data to list
            for datetime_local, sensor_value_string in cur:
                sensor_data_list.append([datetime_local, sensor_value_string])

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                # print("MySQL error: Something is wrong with your user name or password")
                sns_logger.error("MySQL error: Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                # print("MySQL error: Database does not exist")
                sns_logger.error("MySQL error: Database does not exist")
            else:
                # print(err)
                sns_logger.error(f"Error:{err}")
        else:
            # print("MySQL Connection OK!")
            sns_logger.debug("MySQL Connection OK!")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
                
        # jsonify and return list with sensor data 
        return jsonify(sensor_data_list)
        