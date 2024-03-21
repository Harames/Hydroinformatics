# --------------------------------------------------------------
# Created by: Jon Goodall, University of Virginia
# Modified by: Jeff Horsburgh
# Modified for use in assignment by: Matthew Harames
# Last modified on: 3/21/2024
# Description: Plotting time series data in Pandas for class assignment
# --------------------------------------------------------------

# Import statements
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Connect to the database
conn = sqlite3.connect('Logan_River_Temperature_ODM.sqlite')

# SQL statements to grab water temperature at sites 1 and 9
sql_statement1 = "SELECT LocalDateTime, DataValue FROM DataValues " \
                "WHERE SiteID = 1 AND VariableID = 1 " \
                "AND QualityControlLevelID = 1 AND DataValue <> -9999 " \
                "ORDER BY LocalDateTime ASC"

sql_statement2 = "SELECT LocalDateTime, DataValue FROM DataValues " \
                "WHERE SiteID = 9 AND VariableID = 1 " \
                "AND QualityControlLevelID = 1 AND DataValue <> -9999 " \
                "ORDER BY LocalDateTime ASC"

# Get the temperature data into two different dataframes
df1 = pd.read_sql(sql_statement1, conn, index_col='LocalDateTime', parse_dates=['LocalDateTime'])

df2 = pd.read_sql(sql_statement2, conn, index_col='LocalDateTime', parse_dates=['LocalDateTime'])

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))

# Plot temperature data for site 1 as is in top left
df1['DataValue'].plot(ax=axes[0, 0], label='Temperature')
legend = axes[0, 0].legend(loc='upper left', shadow=True)
axes[0, 0].set_title('Temperature at SiteID = 1')
axes[0, 0].set(ylim=(-1, 22.5), yticks=(np.arange(0, 22.5, 2.5)))
axes[0, 0].set_xlabel('Date of Observation')
axes[0, 0].set_ylabel('Degrees Celsius')

# Plot temperature data for site 9 as is in top right
df2['DataValue'].plot(ax=axes[0, 1], label='Temperature')
legend = axes[0, 1].legend(loc='upper left', shadow=True)
axes[0, 1].set_title('Temperature at SiteID = 9')
axes[0, 1].set(ylim=(-1, 22.5), yticks=(np.arange(0, 22.5, 2.5)))
axes[0, 1].set_xlabel('Date of Observation')
axes[0, 1].set_ylabel('Degrees Celsius')

# Plot weekly resampled mean, min, and max temperature data in bottom left for site 1
df1['DataValue'].resample('MS').mean().plot(ax=axes[1, 0], label='Mean')
df1['DataValue'].resample('MS').min().plot(ax=axes[1, 0], label='Min')
df1['DataValue'].resample('MS').max().plot(ax=axes[1, 0], label='Max')
axes[1, 0].set_title("Monthly Resample at SiteID = 1")
axes[1, 0].set(ylim=(-1, 22.5), yticks=(np.arange(0, 22.5, 2.5)))
axes[1, 0].set_xlabel('Date of Observation')
axes[1, 0].set_ylabel('Degrees Celsius')
legend = axes[1, 0].legend(loc='upper left', shadow=True)
plt.xticks(rotation=30)

# Plot weekly resampled mean, min, and max temperature data in bottom left for site 2
df2['DataValue'].resample('MS').mean().plot(ax=axes[1, 1], label='Mean')
df2['DataValue'].resample('MS').min().plot(ax=axes[1, 1], label='Min')
df2['DataValue'].resample('MS').max().plot(ax=axes[1, 1], label='Max')
axes[1, 1].set_title("Monthly Resample at SiteID = 9")
axes[1, 1].set(ylim=(-1, 22.5), yticks=(np.arange(0, 22.5, 2.5)))
axes[1, 1].set_xlabel('Date of Observation')
axes[1, 1].set_ylabel('Degrees Celsius')
legend = axes[1, 1].legend(loc='upper left', shadow=True)
plt.xticks(rotation=30)

# Put everything together, save the figure, and output the plot
fig.suptitle('')
plt.tight_layout()
plt.savefig('LoganRiverTemperature.png')
plt.show()