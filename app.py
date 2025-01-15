from flask import Flask, jsonify, request
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime as dt
import pandas as pd
from collections import OrderedDict #to maintain the order in json returns
import json

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Error Handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request", "message": str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found", "message": str(error)}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal Server Error", "message": str(error)}), 500

# Flask Routes
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"<h2>Available Routes on this Portal (Clickable links):</h2>"
        f"<table border='1' style='width:50%; text-align:left;'>"
        f"<tr><th>Description</br> (Data range 2010-01-01 to 2017-08-23)</th><th>Link</th></tr>"
        f"<tr><td>To Get all the precipitation measurements data</td><td><a href='/api/v1.0/measurements'>/api/v1.0/measurements</a></td></tr>"
        f"<tr><td>To Get all the station data</td><td><a href='/api/v1.0/stations'>/api/v1.0/stations</a></td></tr>"
        f"<tr><td>To Get all the measurements grouped by stations</td><td><a href='/api/v1.0/measurements_Stations'>/api/v1.0/measurements_Stations</a></td></tr>"
        f"<tr><td>To Get all the measurements grouped by stations within a date range</td><td><a href='/api/v1.0/measurements_StationsInRange/2010-01-01/2017-08-23'>/api/v1.0/measurements_StationsInRange/2010-01-01/2017-08-23</a></td></tr>"        
        f"<tr><td>To Get temperature statistics (min, avg, max) for a given date range</td><td><a href='/api/v1.0/temp_stats/2010-01-01/2017-08-23'>/api/v1.0/temp_stats/2010-01-01/2017-08-23</a></td></tr>"
        f"<tr><td>To Get temperature statistics (min, avg, max) for a specific station within a date range</td><td><a href='/api/v1.0/temp_stats_station/USC00519397/2010-01-01/2017-08-23'>/api/v1.0/temp_stats_station/USC00519397/2010-01-01/2017-08-23</a></td></tr>"
        f"</table>"
    )

@app.route("/api/v1.0/measurements")
def get_measurements():
    session = Session(engine)
    try:
        results = session.query(Measurement).all()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

    all_measurements = []
    for measurement in results:
        measurement_dict = OrderedDict({
            "id": measurement.id,
            "station": measurement.station,
            "date": measurement.date,
            "prcp": measurement.prcp,
            "tobs": measurement.tobs
        })
        all_measurements.append(measurement_dict)

    return app.response_class(
        response=json.dumps(all_measurements, sort_keys=False),
        mimetype='application/json'
    )

@app.route("/api/v1.0/stations")
def get_stations():
    session = Session(engine)
    try:
        results = session.query(Station).all()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

    all_stations = []
    for station in results:
        station_dict = OrderedDict({
            "id": station.id,
            "station": station.station,
            "name": station.name,
            "latitude": station.latitude,
            "longitude": station.longitude,
            "elevation": station.elevation
        })
        all_stations.append(station_dict)

    return app.response_class(
        response=json.dumps(all_stations, sort_keys=False),
        mimetype='application/json'
    )

@app.route("/api/v1.0/measurements_Stations")
def get_measurements_by_stations():
    session = Session(engine)
    try:
        results = session.query(
            Measurement.date,
            Measurement.id,
            Measurement.station,
            Station.name,
            Station.latitude,
            Station.longitude,
            Measurement.prcp,
            Measurement.tobs
        ).join(Station, Measurement.station == Station.station).all()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

    joined_data = []
    for date, id, station, name, latitude, longitude, prcp, tobs in results:
        data_dict = OrderedDict({
            "date": date,
            "id": id,
            "station": station,
            "name": name,
            "latitude": latitude,
            "longitude": longitude,
            "prcp": prcp,
            "tobs": tobs
        })
        joined_data.append(data_dict)

    return app.response_class(
        response=json.dumps(joined_data, sort_keys=False),
        mimetype='application/json'
    )

@app.route("/api/v1.0/measurements_StationsInRange/<start_date>/<end_date>")
def get_measurements_by_stations_in_range(start_date, end_date):
    session = Session(engine)
    try:
        results = session.query(
            Measurement.date,
            Measurement.id,
            Measurement.station,
            Station.name,
            Station.latitude,
            Station.longitude,
            Measurement.prcp,
            Measurement.tobs
        ).join(Station, Measurement.station == Station.station).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.date <= end_date).all()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

    joined_data = []
    for date, id, station, name, latitude, longitude, prcp, tobs in results:
        data_dict = OrderedDict({
            "date": date,
            "id": id,
            "station": station,
            "name": name,
            "latitude": latitude,
            "longitude": longitude,
            "prcp": prcp,
            "tobs": tobs
        })
        joined_data.append(data_dict)

    return app.response_class(
        response=json.dumps(joined_data, sort_keys=False),
        mimetype='application/json'
    )

@app.route("/api/v1.0/temp_stats/<start>/<end>")
def temp_stats(start, end):
    session = Session(engine)
    try:
        results = session.query(
            func.min(Measurement.tobs).label("TMIN"),
            func.avg(Measurement.tobs).label("TAVG"),
            func.max(Measurement.tobs).label("TMAX")
        ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

    tmin, tavg, tmax = results[0]

    return app.response_class(
        response=json.dumps(OrderedDict({
            "Start Date": start,
            "End Date": end,
            "Minimum recorded Temperature": tmin,
            "Average recorded Temperature": tavg,
            "Maximum recorded Temperature": tmax
        }), sort_keys=False),
        mimetype='application/json'
    )

@app.route("/api/v1.0/temp_stats_station/<station>/<start>/<end>")
def temp_stats_station(station, start, end):
    session = Session(engine)
    try:
        results = session.query(
            func.min(Measurement.tobs).label("TMIN"),
            func.avg(Measurement.tobs).label("TAVG"),
            func.max(Measurement.tobs).label("TMAX")
        ).filter(Measurement.station == station).\
          filter(Measurement.date >= start).\
          filter(Measurement.date <= end).all()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

    tmin, tavg, tmax = results[0]

    return app.response_class(
        response=json.dumps(OrderedDict({
            "Station": station,
            "Start Date": start,
            "End Date": end,
            "Minimum recorded Temperature": tmin,
            "Average recorded Temperature": tavg,
            "Maximum recorded Temperature": tmax
        }), sort_keys=False),
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(debug=True)
