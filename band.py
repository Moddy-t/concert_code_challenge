import sqlite3


class Band:
    """
    Represents a Band in the database.

    Attributes:
        id (int): Unique identifier for the band in the database.
        name (str): The name of the band.
        hometown (str): The city from which the band is from.
    """

    def __init__(self, id, name, hometown):
        self.id = id
        self.name = name
        self.hometown = hometown

    @staticmethod
    def get(cursor, band_id):
        """
        Finds a Band in the database from its id.
           takes : cursor (sqlite3.Cursor): A database connection.
            band_id (int): The id of the Band to retrieve.
            as argumrents
        Returns:
            Band: The Band with the given id.
        """
        query = "SELECT * FROM bands WHERE id = ?"
        return cursor.execute(query, (band_id,)).fetchone()

    def concerts(self, cursor):
        """
        Retrieves all Concerts that a band has played at.
        Returns:
            list of Concert: All Concerts that a band has played at.
        """
        query = "SELECT * FROM concerts WHERE band_id = ?"
        return cursor.execute(query, (self.id,)).fetchall()

    def venues(self, cursor):
        """
        Retrieves all Venues that a band has played at.
        Returns:
            list of Venue: All Venues that a band has played at.
        """
        query = """
        SELECT DISTINCT v.* FROM venues v
        JOIN concerts c ON v.id = c.venue_id
        WHERE c.band_id = ?
        """
        return cursor.execute(query, (self.id,)).fetchall()

    def play_in_venue(self, cursor, venue_title, date):
        """
        Adds a Concert to the database with the given venue and date.
        """
        venue_id_query = "SELECT id FROM venues WHERE title = ?"
        venue_id = cursor.execute(venue_id_query, (venue_title,)).fetchone()
        if venue_id:
            query = "INSERT INTO concerts (band_id, venue_id, date) VALUES (?, ?, ?)"
            cursor.execute(query, (self.id, venue_id[0], date))
        else:
            raise ValueError("Venue not found")

    def all_introductions(self, cursor):
        """
        Retrieves all possible introductions for a band.
          Returns:
            list of str: All possible introductions for a band.
        """
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
        """
        Retrieves the Band with the most performances.
                Returns:
            tuple: A tuple containing the name of the band and the number of concerts it has performed.
        """
        query = """
        SELECT b.name, COUNT(c.id) as concert_count
        FROM concerts c
        JOIN bands b ON c.band_id = b.id
        GROUP BY b.id
        ORDER BY concert_count DESC
        LIMIT 1
        """
        return cursor.execute(query).fetchone()
