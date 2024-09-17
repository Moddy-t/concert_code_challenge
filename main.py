import sqlite3

# Define the database connection
DATABASE = 'concerts.db'

def create_tables():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create bands table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bands (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        hometown TEXT NOT NULL
    );
    ''')

    # Create venues table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS venues (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        city TEXT NOT NULL
    );
    ''')

    # Create concerts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS concerts (
        id INTEGER PRIMARY KEY,
        band_id INTEGER NOT NULL,
        venue_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (band_id) REFERENCES bands(id),
        FOREIGN KEY (venue_id) REFERENCES venues(id)
    );
    ''')

    conn.commit()
    conn.close()

# Define Band class
class Band:
    def __init__(self, id, name, hometown):
        self.id = id
        self.name = name
        self.hometown = hometown

    @staticmethod
    def get(cursor, band_id):
        query = "SELECT * FROM bands WHERE id = ?"
        return cursor.execute(query, (band_id,)).fetchone()

    def concerts(self, cursor):
        query = "SELECT * FROM concerts WHERE band_id = ?"
        return cursor.execute(query, (self.id,)).fetchall()

    def venues(self, cursor):
        query = """
        SELECT DISTINCT v.* FROM venues v
        JOIN concerts c ON v.id = c.venue_id
        WHERE c.band_id = ?
        """
        return cursor.execute(query, (self.id,)).fetchall()

    def play_in_venue(self, cursor, venue_title, date):
        venue_id_query = "SELECT id FROM venues WHERE title = ?"
        venue_id = cursor.execute(venue_id_query, (venue_title,)).fetchone()
        if venue_id:
            query = "INSERT INTO concerts (band_id, venue_id, date) VALUES (?, ?, ?)"
            cursor.execute(query, (self.id, venue_id[0], date))
        else:
            raise ValueError("Venue not found")

    def all_introductions(self, cursor):
        query = """
        SELECT v.city, b.name, b.hometown
        FROM concerts c
        JOIN venues v ON c.venue_id = v.id
        JOIN bands b ON c.band_id = b.id
        WHERE c.band_id = ?
        """
        concerts = cursor.execute(query, (self.id,)).fetchall()
        return [f"Hello {c['city']}!!!!! We are {c['name']} and we're from {c['hometown']}" for c in concerts]

    @staticmethod
    def most_performances(cursor):
        query = """
        SELECT b.name, COUNT(c.id) as concert_count
        FROM concerts c
        JOIN bands b ON c.band_id = b.id
        GROUP BY b.id
        ORDER BY concert_count DESC
        LIMIT 1
        """
        return cursor.execute(query).fetchone()

# Define Venue class
class Venue:
    def __init__(self, id, title, city):
        self.id = id
        self.title = title
        self.city = city

    @staticmethod
    def get(cursor, venue_id):
        query = "SELECT * FROM venues WHERE id = ?"
        return cursor.execute(query, (venue_id,)).fetchone()

    def concerts(self, cursor):
        query = "SELECT * FROM concerts WHERE venue_id = ?"
        return cursor.execute(query, (self.id,)).fetchall()

    def bands(self, cursor):
        query = """
        SELECT DISTINCT b.* FROM bands b
        JOIN concerts c ON b.id = c.band_id
        WHERE c.venue_id = ?
        """
        return cursor.execute(query, (self.id,)).fetchall()

    def concert_on(self, cursor, date):
        query = "SELECT * FROM concerts WHERE venue_id = ? AND date = ? LIMIT 1"
        return cursor.execute(query, (self.id, date)).fetchone()

    def most_frequent_band(self, cursor):
        query = """
        SELECT b.name, COUNT(c.id) as performance_count
        FROM concerts c
        JOIN bands b ON c.band_id = b.id
        WHERE c.venue_id = ?
        GROUP BY b.id
        ORDER BY performance_count DESC
        LIMIT 1
        """
        return cursor.execute(query, (self.id,)).fetchone()

# Define Concert class
class Concert:
    def __init__(self, id, band_id, venue_id, date):
        self.id = id
        self.band_id = band_id
        self.venue_id = venue_id
        self.date = date

    @staticmethod
    def get(cursor, concert_id):
        query = "SELECT * FROM concerts WHERE id = ?"
        return cursor.execute(query, (concert_id,)).fetchone()

    def band(self, cursor):
        query = "SELECT * FROM bands WHERE id = ?"
        return cursor.execute(query, (self.band_id,)).fetchone()

    def venue(self, cursor):
        query = "SELECT * FROM venues WHERE id = ?"
        return cursor.execute(query, (self.venue_id,)).fetchone()

    def hometown_show(self, cursor):
        query = """
        SELECT v.city, b.hometown
        FROM concerts c
        JOIN bands b ON c.band_id = b.id
        JOIN venues v ON c.venue_id = v.id
        WHERE c.id = ?
        """
        result = cursor.execute(query, (self.id,)).fetchone()
        return result['city'] == result['hometown']

    def introduction(self, cursor):
        query = """
        SELECT v.city, b.name, b.hometown
        FROM concerts c
        JOIN bands b ON c.band_id = b.id
        JOIN venues v ON c.venue_id = v.id
        WHERE c.id = ?
        """
        result = cursor.execute(query, (self.id,)).fetchone()
        return f"Hello {result['city']}!!!!! We are {result['name']} and we're from {result['hometown']}"

def main():
    create_tables()

    # Connect to the database
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
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
    imagine_dragons = Band.get(cursor, 1)
    nirvana = Band.get(cursor, 2)
    print(f"Imagine Dragons: {imagine_dragons}")
    print(f"Nirvana: {nirvana}")

    # Testing Venue Methods
    msg = Venue.get(cursor, 1)
    wembley = Venue.get(cursor, 2)
    print(f"MSG: {msg}")
    print(f"Wembley: {wembley}")

    # Testing Concert Methods
    concert1 = Concert.get(cursor, 1)
    concert2 = Concert.get(cursor, 2)
    print(f"Concert 1 Band: {concert1['band_id']}")
    print(f"Concert 1 Venue: {concert1['venue_id']}")

    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()
