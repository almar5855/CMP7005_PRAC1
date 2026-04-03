
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

    with st.expander('Error'):
        st.write(f'An error was returned from the backend: {response['data']}')  

    return None

st.set_page_config(layout='wide')

selected = nav.render_navbar()
st.title(selected)

col1, col2 = st.columns(2)
with col1:
    regions, date_from, date_to = fc.dataset_filter()

with col2:
    pollution_component_x = fc.component_filter(False, 'X-Axis Filter', 'x-axis-filter')
    pollution_component_y = fc.component_filter(False, 'Y-Axis Filter', 'y-axis-filter')
    pollution_component = [pollution_component_x, pollution_component_y]

data = request_data(ep.SCAT, regions, date_from, date_to, pollution_component)
if data is not None:
    st.pyplot(data)

