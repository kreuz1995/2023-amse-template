!pip install 'SQLAlchemy==1.4.46'
import json
import requests
import sqlite3
import pandas as pd

#-------------------------------------------------------------------------------------------------------------------------------
# 1st Data Source
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

#-------------------------------------------------------------------------------------------------------------------------------
# Data Transformation and Export
#-------------------------------------------------------------------------------------------------------------------------------

# Read the table 'Location_Traffic_Accidents' from the database into a DataFrame
df = pd.read_sql_table('Location_Traffic_Accidents', 'sqlite:///my_database.db')
df_road_signs = pd.read_sql_table('Location_Traffic_Signs', 'sqlite:///my_database.db')

# Perform transformations on the DataFrame
df = df[['UWOCHENTAG', 'UKATEGORIE', 'XGCSWGS84', 'YGCSWGS84']].rename(columns={'UWOCHENTAG': 'Day_of_the_Week', 'UKATEGORIE': 'Categorie_of_the_accident', 'XGCSWGS84': 'Longitude', 'YGCSWGS84': 'Latitude'})
df = df.loc[:, ~df.columns.duplicated()]
mapping = {1: 'Accident_with_Fatalities', 2: 'Accident_with_serious_injuries', 3: 'Accident_with_minor_injuries'}
df['Categorie_of_the_accident'] = df['Categorie_of_the_accident'].map(mapping)

# Replace commas with decimal points in latitude and longitude columns
df['Latitude'] = df['Latitude'].str.replace(',', '.').astype(float)
df['Longitude'] = df['Longitude'].str.replace(',', '.').astype(float)

# Round latitude and longitude columns to 3 decimal places
df['Latitude'] = df['Latitude'].round(3)
df['Longitude'] = df['Longitude'].round(3)

# Export the updated DataFrame to the database table 'Location_Traffic_Accidents'
df.to_sql('Location_Traffic_Accidents', conn, if_exists='replace', index=False)

df_road_signs=df_road_signs[['type', 'longitude','latitude']]

# Round latitude and longitude columns to 4 decimal places
df_road_signs['latitude'] = df_road_signs['latitude'].round(4)
df_road_signs['longitude'] = df_road_signs['longitude'].round(4)
df_road_signs.to_sql('Location_Traffic_Signs', conn, if_exists='replace', index=False)

conn.commit()
conn.close()
