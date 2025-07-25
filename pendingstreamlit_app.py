# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app 
st.title(f":cup_with_straw: Pending Smoothie Orders :cup_with_straw:")
st.write(
  """
  Orders that need to be filled
  """)

cnx = st.connection("snowflake")

session = cnx.session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
#st.dataframe(data=my_dataframe, use_container_width=True)

if my_dataframe:
    # Now we need to put tick, we need to edit the form, for that we call dtaa editor
    editable_df = st.data_editor(my_dataframe) 
    submitted = st.button("Submit")

    if submitted:
        # but see data didnt save it just static, to SOLVE THIS;
        og_dataset = session.table("smoothies.public.orders")
        # get the original orders table
        edited_dataset = session.create_dataframe(editable_df)
        # ✨ Converts the edited data from data_editor back into a Snowpark DataFrame, so Snowflake can use it.
        # Think of this as your updated version of the orders table (user's changes).
        try:
            og_dataset.merge(edited_dataset
                 , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                 , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                )
            st.success("Orders Updated", icon = '👍')
        except:
            st.write("SOmething went wrong!")

else:
    st.success("There are no pending orders right now", icon = '👍')












