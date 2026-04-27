
import streamlit as st
from http import HTTPStatus
from backend_stub import DatasetAPI as api, Endpoint as ep
from components import nav
from components import filter as fc

def request_data(endpoint, regions, date_from, date_to):

    response = api.request(endpoint, regions, date_from, date_to)

    if response['status'] == HTTPStatus.OK:
        return response['data']

    with st.expander('Error'):
        st.write(f"An error was returned from the backend: {response['data']}")

    return None

st.set_page_config(layout='wide')

selected = nav.render_navbar()

with st.sidebar:
    st.markdown("#### Filters")
    regions, date_from, date_to = fc.dataset_filter()

st.title('Dataset Information')
st.subheader('An overview of the dataset')
st.text('Use the filter in the sidebar to select specific region(s) to explore high-level information about the dataset.')

with st.container(border=True):
    st.markdown('## Dataset Description')
    st.dataframe(request_data(ep.DESC, regions, date_from, date_to))

left1, right1 = st.columns(2, gap="large")

with left1:
    with st.container(border=True):
        st.markdown('## Column Info')
        data = request_data(ep.COLUMNS, regions, date_from, date_to)
        st.dataframe(data)

with right1:
    with st.container(border=True):
        st.markdown("## Missing Values")
        data = request_data(ep.NANS, regions, date_from, date_to)
        if data is not None:
            st.write(data)

st.divider()

left2, right2 = st.columns(2, gap="large")

with left2:
    with st.container(border=True):
        st.markdown('## Dataset Info')
        data = request_data(ep.INFO, regions, date_from, date_to)
        if data is not None:
            st.code(data)

with right2:  
    with st.container(border=True):  
        st.markdown("## Dataset Shape")
        data = request_data(ep.SHAPE, regions, date_from, date_to)
        if data is not None:
            st.metric('Rows', f'{data[0]:,}')
            st.metric('Columns', f'{data[1]:,}')
