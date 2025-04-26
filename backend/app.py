# app.py - EcoVision: Climate Visualizer API
# This file contains basic Flask setup code to get you started.
# You may opt to use FastAPI or another framework if you prefer.

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mysqldb import MySQL
import os
from datetime import datetime

from queries import Queries as q

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MySQL Configuration
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'climate_data')
mysql = MySQL(app)

# Quality weights to be used in calculations
QUALITY_WEIGHTS = {
    'excellent': 1.0,
    'good': 0.8,
    'questionable': 0.5,
    'poor': 0.3
}

@app.route('/api/v1/climate', methods=['GET'])
def get_climate_data():
    """
    Retrieve climate data with optional filtering.
    Query parameters: location_id, start_date, end_date, metric, quality_threshold
    
    Returns climate data in the format specified in the API docs.
    """
    location_id = request.args.get('location_id', type=int)
    start_date = request.args.get('start_data', type=str)
    end_date = request.args.get('end_data', type=str)
    metric = request.args.get('metric', type=str)
    quality_threshold = request.args.get('quality_threshold', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = 50

    def map_row(row):
        (id, location_id, location_name, latitude, longitude, date, metric, value, unit, quality) = row
        return {
            "id": id,
            "location_id": location_id,
            "location_name": location_name,
            "latitude": latitude,
            "longitude": longitude,
            "date": datetime.strftime(date, '%Y-%m-%d'),
            "metric": metric,
            "value": value,
            "unit": unit,
            "quality": quality
        }
    
    cursor = mysql.connection.cursor()

    cursor.execute(q.validate_metric, {'metric': metric})
    rows = cursor.fetchall()
    if len(rows) == 1:
        metric_id = rows[0][0]
    else:
        metric_id = None
        # Could raise Error here
    
    cursor.execute(q.validate_quality_threshold, {'quality_threshold': quality_threshold})
    rows = cursor.fetchall()
    if len(rows) == 1:
        quality_threshold_order = rows[0][0]
    else:
        quality_threshold_order = None
        # Could raise Error here

    select_query, count_query, args = q.get_climate_data(
        location_id,
        start_date,
        end_date,
        metric_id,
        quality_threshold_order,
        page,
        per_page
    )

    cursor.execute(count_query, args)
    count = cursor.fetchone()[0]

    cursor.execute(select_query, args)
    rows = cursor.fetchall()
    data = [map_row(row) for row in rows]
    cursor.close()
    return jsonify({"data": data, "meta": {"total_count": count, "page": page, "per_page": per_page}})
    

@app.route('/api/v1/locations', methods=['GET'])
def get_locations():
    """
    Retrieve all available locations.
    
    Returns location data in the format specified in the API docs.
    """
    def map_row(row):
        (id, name, country, latitude, longitude, region) = row
        return {
            "id": id,
            "name": name,
            "country": country,
            "latitude": latitude,
            "longitude": longitude,
            "region": region
        }
    cursor = mysql.connection.cursor()
    cursor.execute(q.get_locations)
    rows = cursor.fetchall()
    data = [map_row(row) for row in rows]
    cursor.close()
    return jsonify({"data": data})

@app.route('/api/v1/metrics', methods=['GET'])
def get_metrics():
    """
    Retrieve all available climate metrics.
    
    Returns metric data in the format specified in the API docs.
    """
    def map_row(row):
        (id, name, display_name, unit, description) = row
        return {
            "id": id,
            "name": name,
            "display_name": display_name,
            "unit": unit,
            "description": description
        }
    
    cursor = mysql.connection.cursor()
    cursor.execute(q.get_metrics)
    rows = cursor.fetchall()
    data = [map_row(row) for row in rows]
    cursor.close()
    return jsonify({"data": data})

@app.route('/api/v1/summary', methods=['GET'])
def get_summary():
    """
    Retrieve quality-weighted summary statistics for climate data.
    Query parameters: location_id, start_date, end_date, metric, quality_threshold
    
    Returns weighted min, max, and avg values for each metric in the format specified in the API docs.
    """
    # TODO: Implement this endpoint
    # 1. Get query parameters from request.args
    # 2. Validate quality_threshold if provided
    # 3. Get list of metrics to summarize
    # 4. For each metric:
    #    - Calculate quality-weighted statistics using QUALITY_WEIGHTS
    #    - Calculate quality distribution
    #    - Apply proper filtering
    # 5. Format response according to API specification
    
    return jsonify({"data": {}})

@app.route('/api/v1/trends', methods=['GET'])
def get_trends():
    """
    Analyze trends and patterns in climate data.
    Query parameters: location_id, start_date, end_date, metric, quality_threshold
    
    Returns trend analysis including direction, rate of change, anomalies, and seasonality.
    """
    # TODO: Implement this endpoint
    # 1. Get query parameters from request.args
    # 2. Validate quality_threshold if provided
    # 3. For each metric:
    #    - Calculate trend direction and rate of change
    #    - Identify anomalies (values > 2 standard deviations)
    #    - Detect seasonal patterns if sufficient data
    #    - Calculate confidence scores
    # 4. Format response according to API specification
    
    return jsonify({"data": {}})

if __name__ == '__main__':
    app.run(debug=True)

# Optional: FastAPI Implementation boilerplate
"""
To implement the API using FastAPI instead of Flask:

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, List, Any
import databases
import os

# Database connection
DATABASE_URL = f"mysql://{os.environ.get('MYSQL_USER', 'root')}:{os.environ.get('MYSQL_PASSWORD', '')}@{os.environ.get('MYSQL_HOST', 'localhost')}/{os.environ.get('MYSQL_DB', 'climate_data')}"
database = databases.Database(DATABASE_URL)

app = FastAPI(title="EcoVision API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Implement endpoints following the API specification in docs/api.md
"""