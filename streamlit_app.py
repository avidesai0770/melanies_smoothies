# Import required packages
import streamlit as st
from snowflake.snowpark.functions import col

# Title and description
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

# Connect to Snowflake using Streamlit connection
cnx = st.connection("snowflake")  # Assumes you set this up in secrets.toml
session = cnx.session()

# Name input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on the smoothie will be", name_on_order)

# Get fruit list from Snowflake
fruit_df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
fruit_list = [row["FRUIT_NAME"] for row in fruit_df.collect()]  # Convert to Python list

# Multiselect fruit options
ingredients_list = st.multiselect("Choose up to 5 ingredients:", fruit_list, max_selections=5)

# If any ingredients are selected
if ingredients_list:
    # Join selected ingredients as a comma-separated string
    ingredients_string = ", ".join(ingredients_list)

    # SQL insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # Show query (for debug)
    st.write(my_insert_stmt)

    # Button to submit the order
    if st.button("Submit Order"):
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}! ✅")
