# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """
  Choose the fruits you want in your custom Smoothie!
  """)
name_on_order = st.text_input("Name on Smoothie:", "Name")
st.write("The name on your smoothie will be:  ", name_on_order)

# OG STreamlit we cant use get_Active  session that from snowpark libarary, will use different one
cnx = st.connection("snowflake")

session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: ',
    my_dataframe # we can multislect fruits from the dataframe wee made
    , max_selections=5
)

#st.write(ingredients_list) # this will show what we seletc
#st.text(ingredients_list) # this will change selection to list

# here is an issue, if we didnt slect anything empty [] is tehre
# so how to gte rid of it; we can use IF statementn for that

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string =''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        # st.text(smoothiefroot_response.json())
        sf_df = st.dataframe(smoothiefroot_response.json(), use_container_width=True)
        

    st.write(ingredients_string)
    # now will insert this to order table
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order +"""')"""

    st.write(my_insert_stmt)

    # will insert submmit btn; this will avoid feeding each and 
    # every step fruit slection to order table
    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered!, {name_on_order}!", icon="✅")
# ------------------------------------------------------------------------------------------------------------------------------
# Adding daatfrom API












