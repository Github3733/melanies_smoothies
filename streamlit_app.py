# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import snowflake.connector
from snowflake.snowpark.session import Session      
import requests
import pandas as pd

# Add Snowflake connection configuration
snowflake_config = {
    "account": "IKZHEYI-WYB47314",
    "user": "alekhyan",
    "password": "TeklinkHgs008*",
    "role": "SYSADMIN",  
    "warehouse": "COMPUTE_WH",
    "database": "SMOOTHIES",
    "schema": "PUBLIC",
}

# Create Snowflake session (no get_active_session used)
session = Session.builder.configs(snowflake_config).create()

# Write directly to the app
st.title(f"Customize Your Smoothie!:cup_with_straw:")
st.write(
    """Choose the fruits you want in your
    Custom Smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

# Query fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

# Multiselect for ingredients
ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
            ingredients_string+=fruit_chosen+' '
            st.subheader(fruit_chosen + ' Nutrition Information')
            smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
            st_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True) 
            

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


