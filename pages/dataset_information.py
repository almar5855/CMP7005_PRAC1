
import streamlit as st
from http import HTTPStatus
from backend_stub import DatasetAPI as api, Endpoint as ep
from components import nav
from components import filter as fc

def request_data(endpoint, regions, date_from, date_to):

    response = api.request(endpoint, regions, date_from, date_to)

    if response['status'] == HTTPStatus.OK:
        return response['data']

    raise Exception(f'An error occurred {response['status']}')  

st.set_page_config(layout='wide')

selected = nav.render_navbar()
st.title(selected)

regions, date_from, date_to = fc.dataset_filter()

st.markdown('## Dataset Description')
st.dataframe(request_data(ep.DESC, regions, date_from, date_to))

col1, col2 = st.columns(2)

with col1:
    st.markdown("## Dataset Shape")
    data = request_data(ep.SHAPE, regions, date_from, date_to)
    st.write(f'Rows: {data[0]}')
    st.write(f'Columns: {data[1]}')

    st.markdown("## Dataset NANs")
    data = request_data(ep.NANS, regions, date_from, date_to)
    st.write(data)

with col2:
    st.markdown('## Column Info')
    data = request_data(ep.COLUMNS, regions, date_from, date_to)
    st.write(data)

st.markdown('## Dataset Info')
data = request_data(ep.INFO, regions, date_from, date_to)
st.text(data)
