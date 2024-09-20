import sqlite3
class Venue:
    """
    Represents a Venue in the database.

    Attributes:
        id (int): Unique identifier for the venue in the database.
        title (str): The name of the venue.
        city (str): The city in which the venue is located.
    """

    def __init__(self, id, title, city):
        self.id = id
        self.title = title
        self.city = city

    @staticmethod
    def get(cursor, venue_id):
        """
        Finds a Venue in the database from its id.

        takes:
            cursor (sqlite3.Cursor): A database connection.
            venue_id (int): The id of the Venue to retrieve.

        Returns:
            Venue: The Venue with the given id, or None if none exists.
        """
        query = "SELECT * FROM venues WHERE id = ?"
        return cursor.execute(query, (venue_id,)).fetchone()

    def concerts(self, cursor):
        """
        Retrieves all Concerts that take place at this Venue.
        Returns:
            list of Concert: All Concerts that take place at this Venue.
        """
        query = "SELECT * FROM concerts WHERE venue_id = ?"
        return cursor.execute(query, (self.id,)).fetchall()

    def bands(self, cursor):
        """
        Retrieves all Bands that have performed at this Venue.
        Returns:
            list of Band: All Bands that have performed at this Venue.
        """
        query = """
        SELECT DISTINCT b.* FROM bands b
        JOIN concerts c ON b.id = c.band_id
        WHERE c.venue_id = ?
        """
        return cursor.execute(query, (self.id,)).fetchall()

    def concert_on(self, cursor, date):
        """
        Retrieves the Concert that takes place at this Venue on a given date.
        Returns:
            Concert: The Concert that takes place at this Venue on the given date, or None if none exists.
        """
        query = "SELECT * FROM concerts WHERE venue_id = ? AND date = ? LIMIT 1"
        return cursor.execute(query, (self.id, date)).fetchone()

    def most_frequent_band(self, cursor):
        """
        Retrieves the Band that has performed at this Venue the most.
            cursor (sqlite3.Cursor): A database connection.

        Returns:
            tuple: A tuple containing the name of the Band and the number of times it has performed at this Venue.
        """
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
