import sqlite3


class Concert:
    """
    Represents a Concert in the database.
    """

    def __init__(self, id, band_id, venue_id, date):
        self.id = id
        self.band_id = band_id
        self.venue_id = venue_id
        self.date = date

    @staticmethod
    def get(cursor, concert_id):
        """
        Finds a Concert in the database from its id.

        takes:
            cursor (sqlite3.Cursor): A database connection.
            concert_id (int): The id of the Concert to retrieve.

        Returns:
            Concert: The Concert with the given id, or None if none exists.
        """
        query = "SELECT * FROM concerts WHERE id = ?"
        return cursor.execute(query, (concert_id,)).fetchone()

    def band(self, cursor):
        """
        Retrieves the Band that is performing at this Concert.
        Returns:
            Band: The Band that is performing at this Concert.
        """
        query = "SELECT * FROM bands WHERE id = ?"
        return cursor.execute(query, (self.band_id,)).fetchone()

    def venue(self, cursor):
        """
        Retrieves the Venue at which this Concert is taking place.
        Returns:
            Venue: The Venue at which this Concert is taking place.
        """
        query = "SELECT * FROM venues WHERE id = ?"
        return cursor.execute(query, (self.venue_id,)).fetchone()

    def hometown_show(self, cursor):
        """
        Determines if the Concert is in the band's hometown.
        Returns:
            bool: True if the Concert is in the band's hometown, False otherwise.
        """
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
        """
        Retrieves a string introduction for the band based on the Concert.
        Returns:
            str: A string introduction for the band based on the Concert.
        """
        query = """
        SELECT v.city, b.name, b.hometown 
        FROM concerts c 
        JOIN bands b ON c.band_id = b.id 
        JOIN venues v ON c.venue_id = v.id 
        WHERE c.id = ?
        """
        result = cursor.execute(query, (self.id,)).fetchone()
        return f"Hello {result['city']}!!!!! We are {result['name']} and we're from {result['hometown']}"
