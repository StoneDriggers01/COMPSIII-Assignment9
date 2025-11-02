# Step 4: Import required libraries
import requests
import re
import sqlite3
from bs4 import BeautifulSoup

# Step 5: Connect to the movies.db database
connection = sqlite3.connect('movies.db')

# Step 6: Create a cursor object
cursor = connection.cursor()

# Step 7: Drop the movies table if it already exists
cursor.execute('''DROP TABLE IF EXISTS movies;''')

# Step 8: Create the movies table
cursor.execute('''
    CREATE TABLE movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        worldwide_gross INTEGER,
        year INTEGER
    );
''')

# Final step: Commit the changes
connection.commit()