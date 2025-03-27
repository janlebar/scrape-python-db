Medicine Data Scraper

Overview

This project consists of a set of Python scripts to scrape medicine names, extract their side effects, and store the data in an SQLite database. The scripts use web scraping techniques to gather information and organize it into structured formats.

Features

Scrapes a list of medicines alphabetically.

Extracts side effects for each medicine.

Stores data in CSV files.

Imports CSV data into an SQLite database.

Prerequisites

Make sure you have the following dependencies installed:

pip install requests beautifulsoup4 pandas sqlite3

You will also need to set the BASE_URL environment variable before running the scripts.

Scripts

1. scrape_medicines.py

Scrapes medicine names alphabetically from the given BASE_URL.

Saves the list of medicines to medicines_list.txt.

Usage:

python scrape_medicines.py

2. scrape_side_effects.py

Reads the medicine names from medicines_list.txt.

Scrapes side effects for each medicine from the BASE_URL.

Saves results into separate CSV files for each letter.

Usage:

python scrape_side_effects.py

3. import_to_db.py

Reads all CSV files with medicine side effects.

Stores the data in an SQLite database (medicine.db).

Usage:

python import_to_db.py

Database Structure

The SQLite database (medicine.db) contains the following table:

CREATE TABLE IF NOT EXISTS medicine_data (
id INTEGER PRIMARY KEY AUTOINCREMENT,
medicine TEXT,
symptoms TEXT
);

Notes

The scripts include delays (time.sleep(5)) to prevent rate limiting.

Ensure BASE_URL is correctly set in the environment before execution.

License

This project is open-source and available for modification and distribution.

Developed for scraping and organizing medicine data efficiently.
