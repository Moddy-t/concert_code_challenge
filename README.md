# Concert Management System

## Overview

The Concert Management System is a Python application that interacts with a SQLite database to manage data about bands, venues, and concerts. The application provides functionality to handle various operations such as querying band and venue information, managing concerts, and performing aggregations to determine the most frequent band or venue.

## Features

- **Band Management**: Create, retrieve, and manage band details.
- **Venue Management**: Create, retrieve, and manage venue details.
- **Concert Management**: Link bands and venues with concerts, retrieve concert details, and check specific conditions.
- **Aggregations and Relationships**: Determine which band has performed the most concerts, which venue has hosted the most frequent band, and more.

## Requirements

- Python3
- SQLite3

## Setup

### 1. Clone the Repository

Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/Moddy-t/concert-management-system.git
cd concert-management-system

2. Create and Populate the Database

Run the main.py script to set up the database schema and insert sample data. This will create the necessary tables (bands, venues, and concerts) and populate them with initial data.

bash

python3 main.py

3. Verify the Setup

After running main.py, the script will print some sample output to verify that the data has been inserted correctly and methods are working as expected. You should see details about bands, venues, and concerts printed to the console.
Code Overview
main.py

    create_tables(): Creates the bands, venues, and concerts tables in the SQLite database.
    Band: A class representing a band with methods to manage band-related operations.
    Venue: A class representing a venue with methods to manage venue-related operations.
    Concert: A class representing a concert with methods to manage concert-related operations.
    main(): Initializes the database, inserts sample data, and tests the functionalities.

## Methods
Band Methods

    get(cursor, band_id): Retrieves a band by its ID.
    concerts(cursor): Retrieves all concerts for the band.
    venues(cursor): Retrieves all venues where the band has performed.
    play_in_venue(cursor, venue_title, date): Adds a new concert for the band at a specified venue and date.
    all_introductions(cursor): Returns introductions for the band at all venues where it has performed.
    most_performances(cursor): Returns the band with the most performances.

## Venue Methods

    get(cursor, venue_id): Retrieves a venue by its ID.
    concerts(cursor): Retrieves all concerts held at the venue.
    bands(cursor): Retrieves all bands that have performed at the venue.
    concert_on(cursor, date): Finds the first concert at the venue on a specified date.
    most_frequent_band(cursor): Returns the band that has performed the most at the venue.

## Concert Methods

    get(cursor, concert_id): Retrieves a concert by its ID.
    band(cursor): Retrieves the band for the concert.
    venue(cursor): Retrieves the venue for the concert.
    hometown_show(cursor): Checks if the concert is in the band's hometown.
    introduction(cursor): Returns the band's introduction for the concert.