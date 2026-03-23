
import streamlit as st
from streamlit_option_menu import option_menu
import requests

BASE_URL = "http://127.0.0.1:8000"

st.header("Hello")
response = requests.get(f"{BASE_URL}/hello")
if response.status_code == 200:

    st.write(response.json())
else:
    st.write("Not found.")

# with st.sidebar:
#     selected = option_menu(
#         menu_title='Navigation',
#         options=['Home', 'Dataset Understanding', 'Data Preprocessing', 'Statisitical Analysis', 'Modeling'],
#         icons=['house', 'list-task', 'gear', 'graph-up', 'gear'],
#         menu_icon="cast",
#         default_index=0,
#     )
# st.title(f'{selected}')
