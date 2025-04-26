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
            quality_order INT,
            PRIMARY KEY (id)
        );
    '''

    insert_quality_with_id = '''
        INSERT INTO quality 
        (id, name, weight, quality_order)
        VALUES
        (%(id)s, %(name)s, %(weight)s, %(order)s);
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

    get_locations = '''
        SELECT 
            id, 
            name, 
            country, 
            latitude, 
            longitude, 
            region
        FROM location
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

    get_metrics = '''
        SELECT
            id,
            name,
            display_name,
            unit,
            description
        FROM metric
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
    @staticmethod
    def get_climate_data(location_id, start_date, end_date, metric_id, quality_threshold_order, page, per_page):
        """
        Creates queries to get climate data based on args.
        returs a (select_query, count_query, args) tuple.
        Run each query with the provided args to get the results.

        I'd probably look in to trynig to get all queries to act a bit more like this one.
        Retrurning a "query" and an "args" instead of having to rely on knowing what the replacement values are.
        Probably create a datatype that manages that.  Or some other abstraction stuff. 
        I'm not happy with the consistentcy here.  But it's functioning.
        """

        count_query = '''
            SELECT
                COUNT(*)
            FROM climate_data cd
            LEFT JOIN quality q
            ON cd.quality_id = q.id
            LEFT JOIN metric m
            ON cd.metric_id = m.id
            LEFT JOIN location l
            ON cd.location_id = l.id
        '''
        select_query = '''
            SELECT
                cd.id,
                cd.location_id,
                l.name as location_name,
                l.latitude,
                l.longitude,
                cd.date,
                m.name as metric,
                cd.value,
                m.unit,
                q.name as quality
            FROM climate_data cd
            LEFT JOIN quality q
            ON cd.quality_id = q.id
            LEFT JOIN metric m
            ON cd.metric_id = m.id
            LEFT JOIN location l
            ON cd.location_id = l.id
        '''
        args = {}
        wheres = []
        if location_id is not None:
            wheres.append('l.id = %(location_id)s')
            args['location_id'] = location_id
        if start_date is not None:
            wheres.append('cd.date > %(start_date)s')
            args['start_date'] = start_date
        if end_date is not None:
            wheres.append('cd.date < %(end_date)s')
            args['end_date'] = end_date
        if metric_id is not None:
            wheres.append('m.id = %(metric)s')
            args['metric'] = metric_id
        if quality_threshold_order is not None:
            wheres.append('q.quality_order <= %(quality_threshold)s')
            args['quality_threshold'] = quality_threshold_order
        
        if wheres:
            clause = ' AND '.join(wheres)
            select_query = select_query + ' WHERE ' + clause
            count_query = count_query + ' WHERE ' + clause

        select_query = select_query + ' LIMIT %(limit)s  OFFSET %(offset)s '
        args['offset'] = (page - 1) * per_page
        args['limit'] = per_page
        return select_query, count_query, args

    insert_climate_data_with_id = '''
        INSERT INTO climate_data 
        (id, location_id, metric_id, date, value, quality_id)
        VALUES
        (%(id)s, %(location_id)s, %(metric_id)s, %(date)s, %(value)s, %(quality_id)s)
    '''

    validate_metric = '''
        SELECT id from metric 
        WHERE name = %(metric)s
    '''

    validate_quality_threshold = '''
        SELECT quality_order from quality
        WHERE name = %(quality_threshold)s
    '''