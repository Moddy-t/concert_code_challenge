import sqlite3
from db import create_tables
from band import Band
from venue import Venue
from concert import Concert

# Define the database name
DATABASE = 'concerts.db'


def main():
    """
    Main entry point for the program.

    This function performs the following operations:
    1. Creates the database tables
    2. Connects to the database
    3. Inserts sample data into the database
    4. Commits the changes
    5. Tests the Band, Venue, and Concert classes
    6. Closes the connection
    """

    # Create the database tables
    create_tables()

    # Connect to the database
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Enable access to columns by name
    cursor = conn.cursor()

    # Insert sample data
    cursor.execute("INSERT INTO bands (name, hometown) VALUES ('Imagine Dragons', 'London')")
    cursor.execute("INSERT INTO bands (name, hometown) VALUES ('Nirvana', 'Seattle')")
    cursor.execute("INSERT INTO venues (title, city) VALUES ('Madison Square Garden', 'New York')")
    cursor.execute("INSERT INTO venues (title, city) VALUES ('Wembley Stadium', 'London')")
    cursor.execute("INSERT INTO concerts (band_id, venue_id, date) VALUES (1, 1, '2023-09-01')")
    cursor.execute("INSERT INTO concerts (band_id, venue_id, date) VALUES (2, 2, '2023-09-05')")

    # Commit the changes
    conn.commit()

    # Testing Band Methods
    print("Testing Band Methods")
    imagine_dragons = Band.get(cursor, 1)
    nirvana = Band.get(cursor, 2)
    print(f"Imagine Dragons: {imagine_dragons}")
    print(f"Nirvana: {nirvana}")

    # Testing Venue Methods
    print("Testing Venue Methods")
    msg = Venue.get(cursor, 1)
    wembley = Venue.get(cursor, 2)
    print(f"MSG: {msg}")
    print(f"Wembley: {wembley}")

    # Testing Concert Methods
    print("Testing Concert Methods")
    concert1 = Concert.get(cursor, 1)
    concert2 = Concert.get(cursor, 2)
    print(f"Concert 1 Band: {concert1['band_id']}")
    print(f"Concert 1 Venue: {concert2['venue_id']}")

    # Close the connection
    conn.close()


if __name__ == "__main__":
    main()