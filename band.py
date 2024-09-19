import sqlite3

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