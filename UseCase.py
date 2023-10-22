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

