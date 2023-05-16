import json
import requests
import sqlite3
import pandas as pd


#-------------------------------------------------------------------------------------------------------------------------------
#1st Data Source
#-------------------------------------------------------------------------------------------------------------------------------

# Fetch the JSON data
response = requests.get('https://www.mcloud.de/downloads/mcloud/722EDEC3-38BA-4FE2-B087-18C0434CA34E/traffic_sign_analysis.json')

# Load the JSON data
data = response.json()

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('my_database.db')

# Create a cursor object
cur = conn.cursor()

# Create a new table (if it doesn't already exist)
cur.execute('''
    CREATE TABLE IF NOT EXISTS Location_Traffic_Signs (
        timeSinceStartMs REAL,
        type TEXT,
        longitude REAL,
        latitude REAL
    )
''')

# Insert data into the table
for entry in data:
    lon, lat = entry['lon_lat']
    cur.execute('''
        INSERT INTO Location_Traffic_Signs (timeSinceStartMs, type, longitude, latitude) 
        VALUES (?, ?, ?, ?)
    ''', (entry['timeSinceStartMs'], entry['type'], lon, lat))

conn.commit()


#-----------------------------------------------------------------------------------------------------------------------
#2nd data source
#-----------------------------------------------------------------------------------------------------------------------


import io

# Fetch the data
response = requests.get('https://download.statistik-berlin-brandenburg.de/8a7423663f039221/892d24383b99/AfSBBB_BE_LOR_Strasse_Strassenverkehrsunfaelle_2020_Datensatz.csv')

# Create a file-like object from the response text
data = io.StringIO(response.text)

# Load the data into a DataFrame
df = pd.read_csv(data, delimiter=';', encoding='ISO-8859-1')

# # Rename columns if necessary
# df = df.rename(columns={
#     'OBJECTID': 'ObjectID',
#     'LAND': 'Land',
#     'BEZ': 'Bezirk',  # Example of changing original name
#     # Add other columns that you want to rename here
# })

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('my_database.db')

# Export the data to an SQL table
df.to_sql('Location_Traffic_Accidents', conn, if_exists='replace', index=False)

conn.commit()
# Close the connection
conn.close()
