# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be: ', name_on_order)

# Get the Active Session
#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

# Create variable and pull data from Fruit Options
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Create multi select with data from Fruit Options
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections = 5
)

if ingredients_list:

    # Create variable that is a STRING data type
    ingredients_string = ''

    # For loop to convert LIST data type to STRING data type
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # Create variable with INSERT statement
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    # Write variable to screen for testing
    #st.write(my_insert_stmt)
    #st.stop()

    # Create a Submit Order button
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        # Execute INSERT statement
        session.sql(my_insert_stmt).collect()

        # Display success message on screen
        st.success('Your Smoothie is ordered, ' + name_on_order +'!', icon="✅")

# New section to display fruityvice nutrition information
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response)
