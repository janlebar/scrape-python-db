import os
import sqlite3
import pandas as pd
import glob

# Database connection
db_path = "medicine.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table with only necessary columns
cursor.execute("""
CREATE TABLE IF NOT EXISTS medicine_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine TEXT,
    symptoms TEXT
);
""")
conn.commit()

# Read all CSV files matching the pattern
csv_files = glob.glob("medicine_side_effects_*.csv")

for file in csv_files:
    df = pd.read_csv(file)

    # Ensure the CSV has the correct columns
    if "Medicine" not in df.columns or "SideEffects" not in df.columns:
        print(f"Skipping {file}: Incorrect column names.")
        continue
    
    # Insert data into the database
    for _, row in df.iterrows():
        cursor.execute("""
        INSERT INTO medicine_data (medicine, symptoms)
        VALUES (?, ?);
        """, (row["Medicine"], row["SideEffects"]))

# Commit and close the connection
conn.commit()
conn.close()

print("All CSV files have been imported into SQLite successfully!")