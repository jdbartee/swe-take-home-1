from argparse import ArgumentParser
from dataclasses import dataclass
import os
from pathlib import Path
import MySQLdb
from flask import json
from queries import Queries

quality_ids = {
    'excellent': 1,
    'good': 2,
    'questionable': 3,
    'poor': 4,
}

quality_weights = {
    'excellent': 1.0,
    'good': 0.8,
    'questionable': 0.5,
    'poor': 0.3
}


@dataclass
class Location:
    id: int
    name: str
    country: str
    latitude: float
    longitude: float
    region: str

    @staticmethod
    def parse(data_dict):
        return Location(**data_dict)

@dataclass
class Metric:
    id: int
    name: str
    display_name: str
    unit: str
    description: str

    @staticmethod
    def parse(data_dict):
        return Metric(**data_dict)

@dataclass
class ClimateData:
    id: int
    location_id: int
    metric_id: int
    date: str
    value: float
    quality_id: int

    @staticmethod
    def parse(data_dict):
        quality = data_dict.pop('quality', 'poor')
        data_dict['quality_id'] = quality_ids.get(quality, quality_ids['poor'])
        return ClimateData(**data_dict)


def parse_data(data_dict):
    result_dict = {}
    result_dict['locations'] = [Location.parse(location) for location in data_dict['locations']]
    result_dict['metrics'] = [Metric.parse(metric) for metric in data_dict['metrics']]
    result_dict['climate_data'] = [ClimateData.parse(climate_data) for climate_data in data_dict['climate_data']]
    return result_dict



def create_sample(args):
    mysql_host = os.environ.get('MYSQL_HOST', 'localhost')
    mysql_user = os.environ.get('MYSQL_USER', 'root')
    mysql_password  = os.environ.get('MYSQL_PASSWORD', '')
    mysql_database = os.environ.get('MYSQL_DB', 'climate_data')
    data_path = args.data_file

    data = json.load(data_path.open())
    data = parse_data(data)

    q = Queries(mysql_database)

    connection = MySQLdb.connect(host=mysql_host, user=mysql_user, password=mysql_password)
    cursor = connection.cursor()
    cursor.execute(q.drop_db)
    cursor.execute(q.create_db)
    cursor.execute(q.use_db)

    cursor.execute(q.create_quality_table)
    for quality in quality_ids.keys():
        cursor.execute(q.insert_quality_with_id, {
            "id": quality_ids[quality],
            "name": quality,
            "weight": quality_weights[quality]
        })

    cursor.execute(q.create_location_table)
    for location in data['locations']:
        cursor.execute(q.insert_location_with_id, {
            "id": location.id,
            "name": location.name,
            "country": location.country,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "region": location.region
        })

    cursor.execute(q.create_metric_table)
    for metric in data['metrics']:
        metric: Metric
        cursor.execute(q.insert_metric_with_id, {
            "id": metric.id,
            "name": metric.name,
            "display_name": metric.display_name,
            "unit": metric.unit,
            "description": metric.description
        })
    
    cursor.execute(q.create_climate_data_table)
    for climate_data in data['climate_data']:
        climate_data: ClimateData
        cursor.execute(q.insert_climate_data_with_id, {
            "id": climate_data.id,
            "location_id": climate_data.location_id,
            "metric_id": climate_data.metric_id,
            "date": climate_data.date,
            "value": climate_data.value,
            "quality_id": climate_data.quality_id
        })
    
    # TODO: ADD Indexes 



    cursor.close()
    connection.commit()
    connection.close()
    

def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(required=True)
    create_sample_parser = subparsers.add_parser('create-sample')
    create_sample_parser.set_defaults(func=create_sample)
    create_sample_parser.add_argument('data_file', type=Path)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
   main()