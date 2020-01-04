import sqlite3

DATABASE_NAME = 'ogame.sqlite'


class DbUtils(object):

    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_NAME)
        self.cursor = self.connection.cursor()
        self.init()

    def init(self):
        for sql in [self.create_users, self.create_planets, self.create_items,
                    self.create_resources, self.create_queues]:
            self.connection.execute(sql)
        self.connection.commit()

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
