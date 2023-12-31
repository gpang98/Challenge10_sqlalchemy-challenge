# import neccesary modules
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Create a Flask app
app = Flask(__name__)

# Create a database connection engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the database tables
Base = automap_base()

#Base.prepare(engine, reflect=True)
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Design the homepage for the app
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

# Design the precipitation page for the app listing all the data available
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the database for precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary to store the results with date as the key and prcp as the value
    precipitation_data = {}
    for date, prcp in results:
        precipitation_data[date] = prcp

    # Return the JSON representation of the dictionary
    return jsonify(precipitation_data)

# Design the station page for the app listing all the stations name
@app.route("/api/v1.0/stations")
def stations():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the database to retrieve a list of stations
    results = session.query(Station.station).all()

    session.close()

    # Create a list to store the station names
    station_list = [station[0] for station in results]

    # Return the list of stations as JSON
    return jsonify(station_list)

# Design the temperature (tobs) page for the app listing past 1 year temperature data
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date one year from the last date in the dataset
    latest_date = session.query(func.max(func.strftime('%Y-%m-%d', Measurement.date))).scalar()
    one_year_ago = (pd.to_datetime(latest_date) - pd.DateOffset(days=365)).date()

    # Calculate the most active station
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).first()
    most_active_station_id = most_active_station[0]

    # Query the database for temperature observations of the most active station for the previous year
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station_id).\
        filter(Measurement.date >= one_year_ago).all()
    
    session.close()

    # Create a list of dictionaries to store date and temperature observations
    tobs_data = [{"date": date, "tobs": tobs} for date, tobs in results]

    # Return the list of temperature observations as JSON
    return jsonify(tobs_data)

# Design the start date page for the app listing TMIN, TAVG and TMAX from a given date (YYY-MM-DD)
@app.route("/api/v1.0/<start>")
def temperature_stats_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    try:
        # Convert the start date string from the URL to a datetime object
        start_date = dt.datetime.strptime(start, '%Y-%m-%d')

        # Check if the start date is outside the available range
        if start_date < dt.datetime(2010, 1, 1) or start_date > dt.datetime(2017, 8, 22):
            raise ValueError("Start date is outside the valid range from 2010-01-01 to 2017-08-22.")

        # Calculate TMIN, TAVG, and TMAX for dates greater than or equal to the specified start date
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).all()
        
        session.close()

        # Check if any data was found for the specified start date
        if not results:
            return jsonify({"error": "No data found for the specified start date."}), 404

        # Create a dictionary to store the result
        temperature_stats = {
            "TMIN": results[0][0],
            "TAVG": results[0][1],
            "TMAX": results[0][2]
        }

        # Return the JSON representation of the result
        return jsonify(temperature_stats)
    
    except ValueError:
        return jsonify({"error": "Change the <start> to the valid date from 2010-01-01 to 2017-08-22. Check date format. Use YYYY-MM-DD format."}), 400


# Design the start and end date page for the app listing TMIN, TAVG and TMAX for a given dtate range in YYYY-MM-DD format.
@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end):
    try:
        # Convert the start and end date strings to datetime objects
        start_date = dt.datetime.strptime(start, '%Y-%m-%d')
        end_date = dt.datetime.strptime(end, '%Y-%m-%d')

        # Check if start and end dates are within the valid range
        valid_start_date = dt.datetime(2010, 1, 1)
        valid_end_date = dt.datetime(2017, 8, 23)

        if start_date < valid_start_date or end_date > valid_end_date:
            raise ValueError("Dates outside the valid range.")

    except ValueError:
        return jsonify({"error": "Change the <start> and <end> to the valid date from 2010-01-01 to 2017-08-23.  Check date format. Use YYYY-MM-DD format."}), 400


    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query temperature statistics for the specified date range
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()
    
    session.close()

    # Create a dictionary to store temperature statistics
    temperature_stats = {
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    # Return the temperature statistics as JSON
    return jsonify(temperature_stats)


if __name__ == "__main__":
    app.run(debug=True)
