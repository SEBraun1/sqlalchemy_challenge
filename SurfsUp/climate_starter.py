#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt


# In[2]:


import numpy as np
import pandas as pd
import datetime as dt


# # Reflect Tables into SQLAlchemy ORM

# In[3]:


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect


# In[4]:


# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# In[5]:


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)


# In[6]:


# View all of the classes that automap found
Base.classes.keys()


# In[7]:


# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station


# In[8]:


# Create our session (link) from Python to the DB
session = Session(engine)


# # Exploratory Precipitation Analysis

# In[9]:


inspector = inspect(engine)
inspector.get_table_names()


# In[10]:


columns = inspector.get_columns('measurement')
for c in columns:
    print(c['name'], c["type"])


# In[11]:


columns = inspector.get_columns('station')
for c in columns:
    print(c['name'], c["type"])


# In[12]:


# Find the most recent date in the data set.
maxdate = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
maxdate


# In[13]:


year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
year_ago


# In[14]:


type(year_ago)


# In[15]:


# Design a query to retrieve the last 12 months of precipitation data and plot the results. 
# Starting from the most recent data point in the database. 
maxdate = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
maxdate

# Calculate the date one year from the last date in data set.
year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
precip = session.query(measurement.date,measurement.prcp).filter(measurement.date>=year_ago).all()
precip

# Save the query results as a Pandas DataFrame and set the index to the date column
precip_df = pd.DataFrame(precip,columns=["Date","Precipitation"])
precip_df

# Sort the dataframe by date
precip_df = precip_df.sort_values(by=['Date']).dropna().reset_index(drop=True)

# Use Pandas Plotting with Matplotlib to plot the data
precip_df.plot(x="Date",y="Precipitation",figsize=(20,10))
plt.ylabel("Inches")


# In[16]:


# Use Pandas to calcualte the summary statistics for the precipitation data
precip_df.describe()


# # Exploratory Station Analysis

# In[17]:


# Design a query to calculate the total number stations in the dataset
active_stations=session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station)
active_stations
num_stations = active_stations.count()
print(f"Number of Stations: {num_stations}")


# In[18]:


# Design a query to find the most active stations (i.e. what stations have the most rows?)
# List the stations and the counts in descending order.
max_active=session.query(measurement.station,func.count(measurement.station)).            group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
max_active
#order_by(func.sum(Invoices.Total).desc()).all()


# In[19]:


# Using the most active station id from the previous query, calculate the lowest, highest, and average temperature.
temps = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).                filter(measurement.station == 'USC00519281').all()

temps


# In[20]:


# Using the most active station id
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
temp_year = session.query(measurement.date,measurement.tobs).filter(measurement.station=='USC00519281').filter(measurement.date>=year_ago).all()
temp_year

# Save the query results as a Pandas DataFrame and set the index to the date column
temp_df = pd.DataFrame(temp_year,columns=["Date","Temperature"])
temp_df

temp_df = temp_df.sort_values(by=['Date']).dropna().reset_index(drop=True)
temp_df.hist(bins=12)
plt.title("Temperature at Station USC00519281")
plt.ylabel("Frequency")
plt.xlabel("Temperature")
plt.legend(['TOBs'])


# # Close session

# In[21]:


# Close Session
session.close()


# In[ ]:




