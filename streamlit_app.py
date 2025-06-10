# Import python packages
import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your smootie! :cup_with_straw: ")
st.write(
  'Choose the fuits you want in your smootie.'
)

# Get the current credentials
cnx=st.connection( "snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select( col( 'FRUIT_NAME'), col( 'SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
pd_df= my_dataframe.to_pandas()
# st.dataframe( pd_df)
ingredients_list= st.multiselect(
    'Choose upto 5', my_dataframe,
    max_selections= 5
)
# st.stop()
if ingredients_list:
    # st.write( ingredients_list)
    st.text( ingredients_list)

    ingredients_string= ''
    for fruit in ingredients_list:
        ingredients_string+= fruit+' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader( fruit + ' nutrition information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
        sf_df= st.dataframe( data= smoothiefroot_response.json(), use_container_width=True)
    st.write( ingredients_string)
# st.text(smoothiefroot_response.json())

    order_name= st.text_input( 'Name to mark the smootie: ')
    st.write( 'Name on cup: ', order_name)

    Option=''
    Option= st.selectbox( 'How do you want to be contacted?', 
                        ( 'Please choose', 'Email', 'SMS', 'Phone call'))
    st.write( '\>\> ', Option)

    purchease= st.button( 'Submit order')
    if purchease:
        my_insert_stmt = """ insert into smoothies.public.orders( name_on_order, ingredients)
                    values ('""" + order_name + """', '""" + ingredients_string + """')"""
        st.write( 'SQL: ', my_insert_stmt)
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

