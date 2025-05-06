# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import snowflake.connector
from snowflake.snowpark.session import Session

# Add Snowflake connection configuration
snowflake_config = {
    "account": "your_account",
    "user": "your_username",
    "password": "your_password",
    "warehouse": "your_warehouse",
    "database": "your_database",
    "schema": "your_schema",
}

# Create Snowflake connection
conn = snowflake.connector.connect(**snowflake_config)

# Create Snowflake session
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

# Existing logic with active session
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen+' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!,', icon="✅")

