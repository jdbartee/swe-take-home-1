All steps assume you are in the `backend` subdirectory.

# Install 
- requires python 3 already installed.
- Create virtual environment.
    `python -m venv venv`
- Activate virtual environment
    `source venv/bin/activate`
- Install requirements
    `python -m pip install requirements.txt`

# Setup database
- db_manage.py script is able to load properly constructed json and create the database for you.
- You can change what MySQL connection to use by updating environment variables:
- DEFAULTS:
    ```bash
        MYSQL_HOST=localhost
        MYSQL_USER=root
        MYSQL_PASSWORD=
        MYSQL_DB=climate_data 
    ```
- run the following script to load up the sample json / create the database / insert the sample data into the database.
    `python db_manage.py create-sample ../data/sample_data.json`

# Start Flask application
- start the app
    `flask --app app run`

- visit `http://127.0.0.1:5000/api/v1/climate` to confirm functionality.

- Currently only `api/v1/climate` `api/v1/metrics` and `api/v1/locations` are hooked up.


# Thoughts

DB Structure seemed very straight forward.  The data very much dictated the sturcture.

The only thing I noticed that I would want to change from just putting the data in as-is is I split "quality" out into it's own table.  And defined an order for the qualities to help with querying by threshold more efficiently.  I also included the weights in the table so - when I got to implementing that functionality - I could potentially allow the database to perform some calculations for me.  This would allow for the potential for summarizing a larger data set without having to have whole dataset move across the wire when performing queries.


Summary data would hopefully be a fairly straightforward implementation here - but I'm trying to keep honest to limiting myself to only a couple of hours of work.


Trend - I haven't really thought about much yet - but would probably have to research some statistical analysis algorithms to be able to implement it properly.

I'd like to have spent more time coming up with a better "code structure" for building / accessing my queries. I do think having the SQL off on it's own file outised of the "logic" of the flask application makes sense.  But the difference between "static" queries and "built" queries (namely the climate data one) could probably be orgaizied better.