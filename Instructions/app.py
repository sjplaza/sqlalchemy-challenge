import numpy as np
import datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)


# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query date and precipation
    prcp_data = (
        session.query(Measurement.date, Measurement.prcp)
        .order_by(Measurement.date)
        .all()
    )

    results_dict = {}
    for result in prcp_data:
        results_dict[result[0]] = result[1]
    return jsonify(results_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Run JSON list of stations from the dataset
    stations = session.query(Station).all()

    station_list = []
    for station in stations:
        station_dict = {}
        station_dict["id"] = station.id
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        station_list.append(station_dict)
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def temperature():
    # Query the dates and temps of most active station for the last year of data.
    station_high_temp = (
        session.query(Measurement.tobs, Measurement.date)
        .filter(Measurement.station == "USC00519281")
        .filter(Measurement.date >= "2017-08-23")
        .order_by(Measurement.date)
        .all()
    )

    temp_list = []
    for temp_list in station_high_temp:
        tobs_dict = {}
        tobs_dict["date"] = station_high_temp.date
        tobs_dict["station"] = station_high_temp.station
        tobs_dict["tobs"] = station_high_temp.tobs
        temp_list.append(tobs_dict)
    return jsonify(temp_list)


if __name__ == "__main__":
    app.run(debug=True)
