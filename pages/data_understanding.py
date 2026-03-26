
import streamlit as st
from http import HTTPStatus
from backend_stub import DatasetAPI as api, Endpoint as ep
from components import nav
from components import filter as fc

def request_data(endpoint, regions, date_from, date_to):

    response = api.request(endpoint, regions, date_from, date_to)

    if response['status'] == HTTPStatus.OK.value:
        return response['data']

    raise Exception(f'An error occurred {response['status']}')  

selected = nav.render_navbar()
st.title(selected)

regions, date_from, date_to = fc.render_filter()

st.markdown("## Dataset Shape")
data = request_data(ep.SHAPE, regions, date_from, date_to)
st.write(data[0])
st.write(data[1])

# st.write(bs.get_dataset_info(regions, date_from, date_to))
# st.dataframe(bs.get_dataset_description(regions, date_from, date_to))
# st.dataframe(bs.get_dataset_nans(regions, date_from, date_to))

