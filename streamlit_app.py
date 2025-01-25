# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """ Choose the Fruits you want in your Smoothie.
    """
)


name_of_order = st.text_input ('name on smoothie:')
st.write ('the name on your smoothie will be:')

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_lists =  st.multiselect(
    'choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_lists:
    # st.write (ingredients_lists)
    # st.text (ingredients_lists)

    ingredients_string =''
    for fruit_chosen in ingredients_lists:
        ingredients_string += fruit_chosen + ' '
    # st.write (ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_of_order+ """')"""
    time_to_insert = st.button('submit order')
    # st.write(my_insert_stmt)
    # st.stop()
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



