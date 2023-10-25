import streamlit
import requests
from urllib.error import URLError

streamlit.title('My Parents New Healthy Dinner')

streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected =streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)


#create the repeatable code block
def get_frutyvice_data(this_fruit_choice):

   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
   return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("please select fruit to get information")
  else:
    back_from_function = get_frutyvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error();
streamlit.write('The user entered ', fruit_choice)

import snowflake.connector

def get_fruit_load_list():
	with my_cnx.cursor()as my_cur:
		my_cur.execute(""select * from fruit_load_list")
		return my_cur.fetchall()
		
# add a button to load the fruit

if streamlit.button('Get Fruit Load list'):
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
	my_data_row = get_fruit_load_list()
	streamlit.dataframe(my_data_row)



add_my_fruit = streamlit.text_input('What would you like to add?','kiwi')
streamlit.write('thanks for adding', add_my_fruit)
my_cur.execute("insert into fruit_load_list values('from streamlit')")
