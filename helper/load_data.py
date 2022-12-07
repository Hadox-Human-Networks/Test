import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv('../../.env')
PG_HOST = os.getenv('POSTGRES_HOST')
PG_PASS = os.getenv('POSTGRES_PASS')
PG_USER = os.getenv('POSTGRES_USER')
PG_PORT = os.getenv('POSTGRES_PORT')
PG_DB   = os.getenv('POSTGRES_DATABASE')


def read_from_csv(csv_file, usecols):
    """Read selected columns from a csv file and create a Pandas DataFrame with the data

    Args:
        csv_file (String): Path to the csv file
        usecols (List): Name(s) of the column(s) to be used

    Returns:
        pandas.DataFrame: Dataframe with the selected columns
    """
    return pd.read_csv(csv_file, usecols=usecols)

def connection_to_postgres():
    """Create PostgreSQL database connection

    Returns:
        cur: Cursor open with Postgres database connection
    """
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(host=PG_HOST, port=PG_PORT, user=PG_USER,
                        password=PG_PASS, database=PG_DB)
        print('Connected to Postgres')
        cur = conn.cursor()
    except Exception as e:
        print(f'Error: {e}')
    return cur

def read_from_postgres(query, columns_names):
    """Read selected columns from a PostgreSQL database file and create a Pandas DataFrame with the data
    The columns in the query and column_names must match

    Args:
        query (String): Query to fetch the selected data from the selected columns
        columns_names (List): Name(s) of the column(s) selected from the query

    Returns:
        pandas.DataFrame: Dataframe with the selected columns
    """
    conn = None
    tuples = None
    try:
        conn = psycopg2.connect(host=PG_HOST, port=PG_PORT, user=PG_USER,
                        password=PG_PASS, database=PG_DB)
        print('Connected to Postgres')

        cur = conn.cursor()
        cur.execute(query)
        tuples = cur.fetchall()
<<<<<<< HEAD
        cur.close()
        
    except Exception as e:
        print(e)
    
=======
    except Exception as e:
        print(f'Error while connecting to Postgres: {e}')
    finally:
        if conn:
            cur.close()
            conn.close()
>>>>>>> aa69b8c853c2c57818ac0b9511d6390fe9480d0d
    return pd.DataFrame(tuples, columns=columns_names)
