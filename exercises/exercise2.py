import pandas as pd
from sqlalchemy import create_engine

# Fetch the CSV data from the source URL
data = pd.read_csv('https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV', sep=';', decimal=',')

# Define the desired data types
dtypes = {'EVA_NR': 'int', 'DS100': 'object', 'IFOPT': 'object', 'NAME': 'object', 'Verkehr': 'object', 'Laenge': 'float', 'Breite': 'float', 'Betreiber_Name': 'object', 'Betreiber_Nr': 'float'}

# Convert the data types
data = data.astype(dtypes)

# First, drop the "Status" column
data = data.drop('Status', axis=1)

# Drop rows with invalid "Verkehr" values
valid_verkehr_values = ["FV", "RV", "nur DPN"]
data = data[data["Verkehr"].isin(valid_verkehr_values)]

# Remove rows with invalid coordinate values
data = data[(data['Laenge'] >= -90) & (data['Laenge'] <= 90)]
data = data[(data['Breite'] >= -90) & (data['Breite'] <= 90)]

# Define the regex pattern for valid "IFOPT" values
pattern = r'^[A-Za-z]{2}:\d+:\d+(?::\d+)?$'
data = data[data['IFOPT'].str.contains(pattern, na=False)]

# Drop rows with empty cells
data = data.dropna()

# Create a SQLite engine using SQLAlchemy
engine = create_engine('sqlite:///trainstops.sqlite')

# Create the table with appropriate SQLite types
table_query = '''
    CREATE TABLE trainstops (
        EVA_NR INTEGER,
        DS100 TEXT,
        IFOPT TEXT,
        NAME TEXT,
        Verkehr TEXT,
        Laenge REAL,
        Breite REAL,
        Betreiber_Name TEXT,
        Betreiber_Nr REAL
    )
'''
with engine.connect() as connection:
    connection.execute(table_query)
    data.to_sql('trainstops', connection, if_exists='replace', index=False)

# Close the engine
engine.dispose()
