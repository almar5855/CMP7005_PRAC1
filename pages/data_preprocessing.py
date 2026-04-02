
import streamlit as st
import backend_stub as bs
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


selected = nav.render_navbar()
st.title(selected)

col1, col2 = st.columns(2)
with col1:
    regions, date_from, date_to = fc.dataset_filter()

with col2:
    pollution_component = fc.component_filter(False)

    # TODO: A lack of unit testing coming home to roost now
    #pollution_component = pollution_component.drop(['No', 'station'])

#regions, date_from, date_to = fc.dataset_filter()

st.write(pollution_component)
data = request_data(ep.HEAT_NA, regions, date_from, date_to, pollution_component)
st.pyplot(data)
