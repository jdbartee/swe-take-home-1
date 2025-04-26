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
```
    MYSQL_HOST=localhost
    MYSQL_USER=root
    MYSQL_PASSWORD=''
    MYSQL_DB='climate_data'
```
- run the following script to load up the sample json / create the database / insert the sample data into the database.
 `python backend/db_manage.py create-sample data/sample_data.json`
