
import streamlit as st
from http import HTTPStatus
from backend_stub import DatasetAPI as api, Endpoint as ep
from components import nav
from components import filter as fc

def request_data(endpoint, regions, date_from, date_to, component):

    response = api.request(endpoint, regions, date_from, date_to, component)

    if response['status'] == HTTPStatus.OK:
        return response['data']

    with st.expander('Error'):
        st.write(f"An error was returned from the backend: {response['data']}")  

    return None

st.set_page_config(layout='wide')

st.title('Home')
st.text("Welcome to the CMP7005 PRAC1 Assessment: From Data to Application Development. we are going to explore the Beijing pollution dataset over the following pages.")
st.text("The navigation menu will appear on every page, allowing you to move from page to page.")
st.text("Filtering menus are context sensitive and change from page to page. The statistical analysis page has the most filter options, allowing you to switch between types of analysis.")
st.divider()
st.subheader("Raw Data")
st.text("Use the Dataset Filter menu to familiarise yourself with the data from individual regions.")

selected = nav.render_navbar('Home')

with st.sidebar:

    st.markdown("#### Filters")
    regions, date_from, date_to = fc.dataset_filter()

data = request_data(ep.DATA, regions, date_from, date_to, None)
if data is not None:
    st.dataframe(data)
