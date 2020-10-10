# import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# setup the database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

# create an app
app = Flask(__name__)


# show available routes
@app.route("/")
def home():
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
    results = (
        session.query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date > "2016-08-23", Measurement.date < "2018-01-01")
        .order_by(Measurement.date)
        .all()
    )
    all_results = []
    for result in results:
        result_dict = {}
        result_dict["date"] = result.date
        result_dict["prcp"] = result.prcp
        all_results.append(result_dict)

    return jsonify(all_results)


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.name).order_by(Station.name).all()
    all_stations = []
    for result in results:
        result_dict = {}
        result_dict["station"] = result.station
        result_dict["name"] = result.name
        all_stations.append(result_dict)

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs2():
    results = (
        session.query(Measurement.date, Measurement.tobs)
        .filter(Measurement.date > "2016-12-31", Measurement.date < "2018-01-01")
        .all()
    )
    all_tobs2 = []
    for result in results:
        result_dict = {}
        result_dict["date"] = result.date
        result_dict["tobs"] = result.tobs
        all_tobs2.append(result_dict)

    return jsonify(all_tobs2)


@app.route("/api/v1.0/<start>/<end>")
def descr(start, end=None):
    if end == None:
        end = (
            session.query(Measurement.date).order_by(Measurement.date.desc()).first([0])
        )
    tobs = pd.read_sql(
        session.query(Measurement.tobs)
        .filter(Measurement.date > start, Measurement.date <= end)
        .statement,
        session.bind,
    )

    tobs_dict = {}
    tobs_dict["TMIN"] = tobs.describe().loc[tobs.describe().index == "min"]["tobs"][0]
    tobs_dict["TAVG"] = tobs.describe().loc[tobs.describe().index == "mean"]["tobs"][0]
    tobs_dict["TMAX"] = tobs.describe().loc[tobs.describe().index == "max"]["tobs"][0]

    return jsonify(tobs_dict)


if __name__ == "__main__":
    app.run(debug=True)
