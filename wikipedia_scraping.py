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

def scrape_wikipedia():
    url = "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Request failed:", e)
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all("table", class_="wikitable")

    # Locate the correct table by caption
    target_table = None
    for table in tables:
        caption = table.find("caption")
        if caption and "highest-grossing films" in caption.get_text(strip=True).lower():
            target_table = table
            break
    if not target_table and tables:
        target_table = tables[0]
    if not target_table:
        print("No suitable table found.")
        return []

    rows = target_table.find_all("tr")
    movie_list = []

    for row in rows[1:]:  # Skip header
        cells = row.find_all("td")
        if len(cells) >= 5:
            # Clean title by removing footnotes and symbols
            title_raw = cells[2]
            for sup in title_raw.find_all("sup"):
                sup.decompose()
            title = title_raw.get_text(strip=True)
            title = re.sub(r"[^\w\s:–'-]", "", title)

            gross = cells[3].get_text(strip=True)
            year = cells[4].get_text(strip=True)

            gross_clean = re.sub(r"[^\d]", "", gross)

            try:
                gross_int = int(gross_clean)
                year_int = int(year)
                movie_list.append({
                    "title": title,
                    "worldwide_gross": gross_int,
                    "Year": year_int
                })
            except ValueError:
                continue

    return movie_list

# Step 9: Scrape and insert movies into the database
movies = scrape_wikipedia()
for movie in movies:
    cursor.execute('''
        INSERT INTO movies (title, worldwide_gross, year)
        VALUES (?, ?, ?);
    ''', (movie['title'], movie['worldwide_gross'], movie['Year']))

# Final step: Commit the changes
connection.commit()
connection.close()