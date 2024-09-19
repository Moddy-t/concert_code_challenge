import sqlite3

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