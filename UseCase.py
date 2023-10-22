import streamlit as st
import os
from snowflake.connector import connect
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env
load_dotenv("creds.env")

# Read Snowflake credentials from environment variables
snowflake_username = os.getenv("snowflake_username")
snowflake_password = os.getenv("snowflake_password")
snowflake_account = os.getenv("snowflake_account")
snowflake_database = os.getenv("snowflake_database")

# Function to get forecast data
def get_forecast_data():
    # Connect to Snowflake
    conn = connect(
        user=snowflake_username,
        password=snowflake_password,
        account=snowflake_account,
        database=snowflake_database
    )


    # Create the forecast model if it doesn't exist (or use your own script to create the model)

    # Execute the forecast model
    cursor = conn.cursor()
    cursor.execute("CALL impressions_forecast!FORECAST(FORECASTING_PERIODS => 14);")
    cursor.close()

    # Execute a query to retrieve the forecast data
    query = """
    SELECT ts, NULL AS actual, forecast, lower_bound, upper_bound
    FROM TABLE(RESULT_SCAN(-1));
    """

    # Fetch the data into a Pandas DataFrame
    df = pd.read_sql(query, conn)

    # Close the Snowflake connection
    conn.close()

    return df

# Function to get actual data
def get_actual_data():
    # Connect to Snowflake
    conn = connect(
        user=snowflake_username,
        password=snowflake_password,
        account=snowflake_account,
        database=snowflake_database
    )

    # Execute a query to retrieve the actual data
    query = """
    SELECT day AS ts, impression_count AS actual
    FROM daily_impressions;
    """
    # Fetch the data into a Pandas DataFrame
    df = pd.read_sql(query, conn)

    # Close the Snowflake connection
    conn.close()

    return df

# Function to check for an anomaly
def check_for_anomaly(date, impressions):
    # Connect to Snowflake
    conn = connect(
        user=snowflake_username,
        password=snowflake_password,
        account=snowflake_account,
        database=snowflake_database
    )

    cursor = conn.cursor()

    # Set a current schema (replace 'your_schema_name' with the actual schema name)
    schema_name = 'DEMO'
    set_schema_query = f"USE SCHEMA {schema_name}"
    cursor.execute(set_schema_query)

    # Create a temporary table to hold the input data
    create_temp_table_query = f"""
    CREATE OR REPLACE TEMPORARY TABLE temp_input_data (
        day TIMESTAMP_NTZ(9),
        impressions NUMBER(5, 0)
    );
    """
    cursor.execute(create_temp_table_query)

    # Insert data into the temporary table
    insert_data_query = f"""
    INSERT INTO temp_input_data (day, impressions) VALUES (TO_TIMESTAMP('{date}'), {impressions});
    """
    cursor.execute(insert_data_query)
    
    # Commit the transaction to ensure data is available
    cursor.execute("COMMIT;")

    # Execute the anomaly detection
    query = f"""
    CALL impression_anomaly_detector!DETECT_ANOMALIES(
        INPUT_DATA => SYSTEM$QUERY_REFERENCE('SELECT * FROM temp_input_data'),
        TIMESTAMP_COLNAME => 'day',
        TARGET_COLNAME => 'impressions'
    );
    """
    cursor.execute(query)
    
    result = cursor.fetchall()

    # Close the Snowflake connection
    conn.close()

    return result

