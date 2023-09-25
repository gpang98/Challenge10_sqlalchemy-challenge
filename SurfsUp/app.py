import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)


print("_"*50)
print(Base.classes.keys())

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def homepage():
    """List all available routes."""
    available_routes = [
        "/api/v1.0/precipitation",
        "/api/v1.0/stations",
        "/api/v1.0/tobs",
        "/api/v1.0/<start>",
        "/api/v1.0/<start>/<end>"
    ]
    return jsonify(available_routes)

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query the database for precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Create a dictionary to store the results with date as the key and prcp as the value
    precipitation_data = {}
    for date, prcp in results:
        precipitation_data[date] = prcp

    # Return the JSON representation of the dictionary
    return jsonify(precipitation_data)


@app.route("/api/v1.0/stations")
def stations():
    # Query the database to retrieve a list of stations
    results = session.query(Station.station).all()

    # Create a list to store the station names
    station_list = [station[0] for station in results]

    # Return the list of stations as JSON
    return jsonify(station_list)



@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate the date one year from the last date in the dataset
    latest_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = pd.to_datetime(latest_date) - pd.DateOffset(years=1)

    # Query the database for temperature observations of the most active station for the previous year
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station_id).\
        filter(Measurement.date >= one_year_ago).all()

    # Create a list of dictionaries to store date and temperature observations
    tobs_data = [{"date": date, "tobs": tobs} for date, tobs in results]

    # Return the list of temperature observations as JSON
    return jsonify(tobs_data)


@app.route("/api/v1.0/<start>")
def temperature_start(start):
    # Query temperature statistics for a given start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    # Create a dictionary to store temperature statistics
    temperature_stats = {
        "start_date": start,
        "min_temperature": results[0][0],
        "avg_temperature": results[0][1],
        "max_temperature": results[0][2]
    }

    # Return the temperature statistics as JSON
    return jsonify(temperature_stats)

@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end):
    # Query temperature statistics for a date range
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    # Create a dictionary to store temperature statistics
    temperature_stats = {
        "start_date": start,
        "end_date": end,
        "min_temperature": results[0][0],
        "avg_temperature": results[0][1],
        "max_temperature": results[0][2]
    }

    # Return the temperature statistics as JSON
    return jsonify(temperature_stats)



    session.close()


if __name__ == '__main__':
    app.run(debug=True)
