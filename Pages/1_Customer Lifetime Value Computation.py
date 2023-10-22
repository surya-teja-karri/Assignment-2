import streamlit as st
import pandas as pd
from snowflake.connector import connect

# Streamlit interface
st.title("Customer Sales Prediction")

# Input fields
st.subheader("Customer Information")
# Input fields
gender = st.selectbox("Gender", ["M", "F"])
marital_status = st.selectbox("Marital Status", ["D", "M", "S", "U", "W"])
credit_rating = st.selectbox("Credit Rating", ["Good", "High Risk", "Low Risk"])
education_status = st.selectbox("Education Status", ["2 yr Degree", "4 yr Degree", "Advanced Degree", "College", "Primary", "Secondary", "Unknown"])
birth_year = st.number_input("Birth Year", value=1990)
dependency_count = st.number_input("Dependency Count", value=1)
total_sales = st.number_input("total sales", value =20000)

if st.button("Predict"):
    # Create a dictionary for one-hot encoding
    input_data_dict = {
        "CD_GENDER_F": [1.0 if gender == "F" else 0.0],
        "CD_GENDER_M": [1.0 if gender == "M" else 0.0],
        "CD_MARITAL_STATUS_D": [1.0 if marital_status == "D" else 0.0],
        "CD_MARITAL_STATUS_M": [1.0 if marital_status == "M" else 0.0],
        "CD_MARITAL_STATUS_S": [1.0 if marital_status == "S" else 0.0],
        "CD_MARITAL_STATUS_U": [1.0 if marital_status == "U" else 0.0],
        "CD_MARITAL_STATUS_W": [1.0 if marital_status == "W" else 0.0],
        "CD_CREDIT_RATING_GOOD": [1.0 if credit_rating == "Good" else 0.0],
        "CD_CREDIT_RATING_HIGHRISK": [1.0 if credit_rating == "High Risk" else 0.0],
        "CD_CREDIT_RATING_LOWRISK": [1.0 if credit_rating == "Low Risk" else 0.0],
        "CD_EDUCATION_STATUS_2YRDEGREE": [1.0 if education_status == "2 yr Degree" else 0.0],
        "CD_EDUCATION_STATUS_4YRDEGREE": [1.0 if education_status == "4 yr Degree" else 0.0],
        "CD_EDUCATION_STATUS_ADVANCEDDEGREE": [1.0 if education_status == "Advanced Degree" else 0.0],
        "CD_EDUCATION_STATUS_COLLEGE": [1.0 if education_status == "College" else 0.0],
        "CD_EDUCATION_STATUS_PRIMARY": [1.0 if education_status == "Primary" else 0.0],
        "CD_EDUCATION_STATUS_SECONDARY": [1.0 if education_status == "Secondary" else 0.0],
        "CD_EDUCATION_STATUS_UNKNOWN": [1.0 if education_status == "Unknown" else 0.0],
        "C_BIRTH_YEAR": [birth_year],
        "CD_DEP_COUNT": [dependency_count],
        "TOTAL_SALES" : [total_sales]
    }

    # Create a DataFrame from the input data
    input_data_df = pd.DataFrame(input_data_dict)
    print(input_data_df)
    
        # Connect to Snowflake
    connection = connect(
        user='surya7887',
        password='Snowflake!123',
        account='qmhbfok-kqb40312',
        warehouse='FE_AND_INFERENCE_WH',
        database='tpcds_xgboost',
        schema='demo'
    )

 # Call Snowflake UDF
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT TPCDS_PREDICT_CLV({','.join(map(str, input_data_df.values[0]))})")
        prediction = cursor.fetchone()[0]

    st.write(f"Predicted Total Sales: {prediction}")


