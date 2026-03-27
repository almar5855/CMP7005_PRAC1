
import streamlit as st
from http import HTTPStatus
from backend_stub import DatasetAPI as api, Endpoint as ep
from components import nav
from components import filter as fc

# TODO: This needs to find one place to live
def request_data(endpoint, regions, date_from, date_to, component):

    response = api.request(endpoint, regions, date_from, date_to, component)

    if response['status'] == HTTPStatus.OK:
        return response['data']

    raise Exception(f'An error occurred {response['status']}')  

st.set_page_config(layout='wide')

selected = nav.render_navbar()
st.title(selected)

regions, date_from, date_to = fc.dataset_filter()
data = request_data(ep.DATA, regions, date_from, date_to, None)
st.dataframe(data)
