from flask import Flask
from flask_restful import Api

# from app.resources.sensors_data import Sensors
from resources.sensors_data import Sensors
# from app.resources.nagios_data import NagiosAggregator
from resources.nagios_data import NagiosAggregator
# from app.resources.backups_data import Backups
from resources.backups_data import Backups

app = Flask(__name__)
api = Api(app)

api.add_resource(Sensors, "/api/v1/sensors/<int:sensor_id>")
api.add_resource(NagiosAggregator, "/api/v1/nagios/<int:host_id>")
api.add_resource(Backups, "/api/v1/backups")

if __name__ == "__main__":
    app.run(host="", port=8030, debug=False)
