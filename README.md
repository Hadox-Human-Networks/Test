# Emotions App 
Web application for the visualization of advanced analytics and intelligent dashboards. 

## Project structure

```
.
├── README.md
├── app
│   ├── README.md
│   ├── __init__.py
│   ├── controllers
│   ├── forms
│   ├── helper
│   ├── ml-models
│   ├── models
│   ├── routes
│   ├── static
│   │   ├── css
│   │   ├── img
│   │   └── js
│   └── templates
├── config.py
├── emotions.py
├── requirements.txt
├── tests
└── venv
```

The project consists of the following main folders
- controllers: contains all the controllers that will handle requests
- forms: contains all the forms used in the app
- helper: contains all the helpers of the project which will be used to handle for supportive and auxiliary functions
- ml-models: contains Machine Learning models
- models: contains the definitions of the databases to be used
- routes: contains all the routes of app
- static: contains all the static files for the app such as js, css, images.
- templates: contains all HTML files
- tests: contains the code for unit tests

## Python Virtual Environment Setup
To create a new virtual environment:
```bash
$ python3 -m venv venv
```
To activate a virtual environment:
```bash
$ source venv/bin/activate
```
To install all the necessary packages:
```bash
(venv) $ python3 -m pip install -r requirements.txt
```
**NOTE**: if an error occurs while installing the packages, upgrade pip command:
```bash
(venv) $ python3 -m pip install --upgrade pip
```

**NOTE 2**: If an error with Bootstrap like "No module named 'flask_bootstrap'" occurs, uninstall and reinstall the Bootstrap packages:
```bash
(venv) $ pip uninstall flask-bootstrap bootstrap-flask
(venv) $ pip install bootstrap-flask flask-bootstrap
```

To deactivate a virtual environment:
```
(venv) $ deactivate
``` 

## Running the app
To run the app, type the following in the command terminal:

```bash
(venv) $ flask run
```

## Database in PostgreSQL
The database engine used in the project is PostgreSQL.

First, the PostgreSQL command terminal is accessed with `psql`. Once inside, the database and the schema where the synthetic data and ML models results will be stored are created.

```
postgres=# CREATE DATABASE winkle;
postgres=# \c winkle
```
### Syntethic data
The `table_schema.sql` file contains the code to create the tables with the structure of the different scenarios of the synthetic data. To create the table:
```
winkle=# CREATE SCHEMA winkle_data;
winkle=# \i '<path_to_table_schema.sql>'
```
Example:

```
winkle=# \i '/Users/username/abinbev/app/table_schema.sql'
```
The synthetic data are located inside the `app/data` folder. 
To copy the data from the csv file is with the following statement:

```sql
COPY winkle_data.scenary_i
FROM '<path_to_csv_file>'
DELIMITER ','
CSV HEADER;
```
Example:
```
winkle=# COPY winkle_data.scenary_i
winkle-# FROM '/Users/username/abinbev/data/Winkle_ABinBev_synt.csv'
winkle-# DELIMITER ','
winkle-# CSV HEADER;
```
### ML models data
The `models_schema.sql` file contains the code to create the tables where the results of ML models will be stored, such as model type, error messages, configuration, update dates, etc.
To create the table:
```
winkle=# CREATE SCHEMA models;
winkle=# \i '<path_to_models_schema.sql>'
```
Example:

```
winkle=# \i '/Users/username/abinbev/app/models_schema.sql'
```
