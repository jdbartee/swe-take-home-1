import re

class Queries:
    def __init__(self, db_name):
        self.validate_db_name(db_name)
        self.db_name = db_name
        self.drop_db = f'DROP DATABASE IF EXISTS {self.db_name};'
        self.create_db = f'CREATE DATABASE {self.db_name};'
        self.use_db = f'USE {self.db_name};'

    @staticmethod
    def validate_db_name(database_name):
        validator = re.compile(r'^[0-9a-zA-Z_\$]+$')
        if not validator.match(database_name):
            raise ValueError(f'Invalid Database Name: {database_name}')

    create_quality_table = '''
        CREATE TABLE quality (
            id INT AUTO_INCREMENT,
            name VARCHAR(255),
            weight FLOAT,
            PRIMARY KEY (id)
        );
    '''

    insert_quality_with_id = '''
        INSERT INTO quality 
        (id, name, weight)
        VALUES
        (%(id)s, %(name)s, %(weight)s);
    '''

    create_location_table = '''
        CREATE TABLE location (
            id INT AUTO_INCREMENT,
            name VARCHAR(255),
            country VARCHAR(255),
            latitude FLOAT,
            longitude FLOAT,
            region VARCHAR(255),
            PRIMARY KEY (id)
        );
    '''

    insert_location_with_id = '''
        INSERT into location 
        (id, name, country, latitude, longitude, region)
        VALUES
        (%(id)s, %(name)s, %(country)s, %(latitude)s, %(longitude)s, %(region)s);
    '''

    create_metric_table = '''
        CREATE TABLE metric (
            id INT AUTO_INCREMENT,
            name VARCHAR(255),
            display_name VARCHAR(255),
            unit VARCHAR(255),
            description VARCHAR(255),
            PRIMARY KEY (id)
        );
    '''

    insert_metric_with_id = '''
        INSERT into metric 
        (id, name, display_name, unit, description)
        VALUES
        (%(id)s, %(name)s, %(display_name)s, %(unit)s, %(description)s);
    '''

    create_climate_data_table = '''
        CREATE TABLE climate_data (
            id INT AUTO_INCREMENT,
            location_id INT,
            metric_id INT,
            date DATE,
            value FLOAT,
            quality_id INT,
            PRIMARY KEY (id),
            FOREIGN KEY (location_id) REFERENCES location(id),
            FOREIGN KEY (metric_id) REFERENCES metric(id),
            FOREIGN KEY (quality_id) REFERENCES quality(id)
        );
    '''

    insert_climate_data_with_id = '''
        INSERT INTO climate_data 
        (id, location_id, metric_id, date, value, quality_id)
        VALUES
        (%(id)s, %(location_id)s, %(metric_id)s, %(date)s, %(value)s, %(quality_id)s)
    '''