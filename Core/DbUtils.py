import sqlite3
from datetime import datetime
from typing import List

DATABASE_NAME = 'ogame.sqlite'


class DbUtils:
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_NAME)
        self.cursor = self.connection.cursor()
        self.init()

    def init(self):
        for sql in [self.create_save_fleet_queue, self.create_return_fleet_queue]:
            self.cursor.execute(sql)
        self.connection.commit()

    def save_fleet(self, planet: str) -> None:
        if planet not in self.get_save_fleet_queue():
            self.cursor.execute(
                'INSERT INTO save_fleet_queue (name) VALUES (?)', (planet,)
            )
            self.connection.commit()

    def return_fleet(self, planet: str, sending_datetime: datetime) -> None:
        if planet not in self.get_return_fleet_queue():
            self.cursor.execute(
                'INSERT INTO return_fleet_queue (name, sending_time) VALUES (?, ?)',
                (planet, str(sending_datetime.timestamp()),)
            )
            self.connection.commit()

    def get_save_fleet_queue(self) -> List:
        cur = self.cursor.execute('SELECT * FROM save_fleet_queue')
        return [el[0] for el in cur.fetchall()]

    def get_return_fleet_queue(self) -> List:
        cur = self.cursor.execute('SELECT name FROM return_fleet_queue')
        return [el[0] for el in cur.fetchall()]

    def get_return_fleet_sending_time(self, planet: str) -> datetime:
        cur = self.cursor.execute('SELECT sending_time '
                                  'FROM return_fleet_queue '
                                  'WHERE name=?', (planet,))
        sending_time = cur.fetchone()[0]
        return datetime.fromtimestamp(float(sending_time))

    def delete_saved_fleet(self, planet: str) -> None:
        self.cursor.execute('DELETE FROM save_fleet_queue WHERE name=?', (planet,))
        self.connection.commit()

    def delete_returned_fleet(self, planet: str) -> None:
        self.cursor.execute('DELETE FROM return_fleet_queue WHERE name=?', (planet,))
        self.connection.commit()

    @property
    def create_save_fleet_queue(self):
        return """CREATE TABLE IF NOT EXISTS save_fleet_queue(name text NOT NULL)"""

    @property
    def create_return_fleet_queue(self):
        return """CREATE TABLE IF NOT EXISTS return_fleet_queue(
        name text NOT NULL,
        sending_time text NOT NULL)"""

    @property
    def create_users(self):
        return """"CREATE TABLE IF NOT EXISTS users(
        id integer UNIQUE PRIMARY KEY,
        email text NOT NULL UNIQUE,
        password text NOT NULL,
        name text NOT NULL)"""

    @property
    def create_planets(self):
        return """CREATE TABLE IF NOT EXISTS planets(
        id integer UNIQUE PRIMARY KEY,
        owner integer,
        name text,
        koordinates text,
        FOREIGN KEY (owner) REFERENCES users (id))"""

    @property
    def create_resources(self):
        return """CREATE TABLE IF NOT EXISTS resources
        (resource_name text NOT NULL,
        planet integer NOT NULL,
        available integer NOT NULL,
        dig_velocity integer,
        storage_capacity integer,
        safe_storage_capacity integer,
        FOREIGN KEY (planet) REFERENCES planets (id))"""

    @property
    def create_items(self):
        return """"CREATE TABLE IF NOT EXISTS items
        (id integer UNIQUE NOT NULL PRIMARY KEY,
        type text NOT NULL,
        name text NOT NULL,
        level integer NOT NULL,
        required_metal integer NOT NULL,
        required_crystal integer NOT NULL,
        required_deyterium integer NOT NULL,
        time text)"""

    @property
    def create_queues(self):
        return """"CREATE TABLE IF NOT EXISTS queues
        (type text NOT NULL,
        planet integer NOT NULL,
        timestamp text NOT NULL,
        item integer NOT NULL,
        count text,
        FOREIGN KEY (planet) REFERENCES planets (id),
        FOREIGN KEY (item) REFERENCES items (id))"""
