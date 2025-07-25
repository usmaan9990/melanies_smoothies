# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

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

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# snowpark dataframe converting to pandas so we can use loc
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: ',
    my_dataframe 
    , max_selections=5
)


if ingredients_list:
  ingredients_string =''
  for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen + ' '
    # will get the value from searchon and tell for x value search keyword is y
    search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON']
        if pd.isna(search_on.iloc[0]):
          search_on = search_on.fillna(fruit_chosen).iloc[0]
        else:
          search_on = search_on.iloc[0]
    
    st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

    st.subheader(fruit_chosen + ' Nutrition Information')
    smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/"+search_on)
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













