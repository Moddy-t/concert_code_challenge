import sqlite3

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