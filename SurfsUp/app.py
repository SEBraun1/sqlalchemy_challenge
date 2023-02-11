import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt

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

# Save reference to the table
measurement = Base.classes.measurement
station =Base.classes.station

#Open Session
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
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    """Convert the query results from your precipitation analysis (i.e. retrieve only
        the last 12 months of data) to a dictionary using date as the key and prcp 
        as the value."""
    #Calculate data for one year ago from most recent date available
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    year_ago
    #Query data for precipitation values
    precip = session.query(measurement.date,measurement.prcp).filter(measurement.date>=year_ago).all()
    precip

    #Place Date & Precip into diction 
    precpdate = {date:prcp for date, prcp in precip}

    session.close()

    return jsonify(precpdate)



@app.route("/api/v1.0/stations")
def stations():

    """Return a JSON list of stations from the dataset."""
    stations=session.query(station.name).all()
    # active_stations
    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)



"""Query the dates and temperature observations of the most-active 
station for the previous year of data.
Return a JSON list of temperature observations for the previous year."""
@app.route("/api/v1.0/tobs")
def tobs():
    #Calculate data for one year ago from most recent date available
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)


    station_year= session.query(measurement.date,measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
            filter(measurement.date>=year_ago).all()

    #Create a list to store query data for dates and temperatures of the most-active station
    active_station = []
    for x, y in station_year:
        station_temp_date = {}
        station_temp_date["Date"] = x
        station_temp_date["TOBs"] = y
        active_station.append(station_temp_date)

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(active_station))

    return jsonify(all_stations)


"""Return a JSON list of the minimum temperature, 
the average temperature, 
and the maximum temperature for a specified start or start-end 
range.

For a specified start, calculate TMIN, TAVG, and TMAX for all 
the dates greater than or equal to the start date."""

@app.route("/api/v1.0/<start>") 
def start_date(start):

    # Query the db for entries equal to the input start date
    start_output = session.query(measurement.date, func.min(measurement.tobs),\
         func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start).all()
    
    # Loop through query results and input into a dictionary.
    start_list = []
    for w, x, y, z in start_output:
            start_dict = {}
            start_dict["Date"] = w
            start_dict["Min"] = x
            start_dict["Max"] = y
            start_dict["Average"] = z
            start_list.append(start_dict)

    session.close()

    return jsonify(start_list)


"""For a specified start date and end date, calculate TMIN, TAVG, 
and TMAX for the dates from the start date to the end date, 
inclusive."""

@app.route("/api/v1.0/<start>/<end>") 
def date_range(start,end):

    # Query the db for entries equal to the input start date and end date
    range = session.query(measurement.date, func.min(measurement.tobs),\
         func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.date >= end).all()
 
    # Loop through query results and input into a dictionary.
    range_list = []
    for w, x, y, z in range:
            range_dict = {}
            range_dict["Date"] = w
            range_dict["Min"] = x
            range_dict["Max"] = y
            range_dict["Average"] = z
            range_list.append(range_dict)

    session.close()

    # Jasonify list results
    return jsonify(range_list)


if __name__ == '__main__':
    app.run(debug=True)