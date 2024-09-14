import csv
import sqlite3
import os

def create_db_from_csv(csv_file, db_name):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Read the CSV file
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)  # Get the headers

        # Create table
        table_name = os.path.splitext(os.path.basename(csv_file))[0]
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{header.replace(' ', '_')} TEXT' for header in headers])})"
        cursor.execute(create_table_query)

        # Insert data
        insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['?' for _ in headers])})"
        cursor.executemany(insert_query, csv_reader)

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print(f"Database '{db_name}' created successfully with table '{table_name}'")

# Usage
csv_file = 'medals_total.csv'
db_name = 'olympics.db'
create_db_from_csv(csv_file, db_name)