#!/bin/bash

# Run the Python script to create the databases and tables
python pipeline.py

# Check if the tables are created

# Specify the path to your SQLite database file
database_file="my_database.db"

# Check if the database file exists
if [ -f "$database_file" ]; then
    echo "Database file $database_file exists."

    # Check if the tables exist in the database
    table1_exists=$(sqlite3 "$database_file" "SELECT name FROM sqlite_master WHERE type='table' AND name='Location_Traffic_Signs';")
    table2_exists=$(sqlite3 "$database_file" "SELECT name FROM sqlite_master WHERE type='table' AND name='Location_Traffic_Accidents';")

    if [ -n "$table1_exists" ] && [ -n "$table2_exists" ]; then
        echo "Tables Location_Road_Signs and Location_Traffic_Accidents exist in the database."
    else
        echo "Tables Location_Traffic_Signs and/or Location_Traffic_Accidents do not exist in the database."
    fi
else
    echo "Database file $database_file does not exist."
fi
