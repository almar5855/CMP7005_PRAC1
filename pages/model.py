
import streamlit as st
from http import HTTPStatus
import backend_stub as bs
from modeling_backend_stub import ModelingAPI as api, Endpoint as ep
from components import nav
from components import filter as fc

def request_data(endpoint):

    response = api.request(endpoint)

    if response['status'] == HTTPStatus.OK:
        return response['data']

    with st.expander('Error'):
        st.write(f"An error was returned from the backend: {response['data']}")

    return None

st.set_page_config(layout='wide')

selected = nav.render_navbar()
st.title('Modeling')

#regions, date_from, date_to = fc.dataset_filter()

with st.sidebar:
    model = fc.model_filter()

if model == 'Linear Regression':
    data = request_data(ep.LINEAR)
    if data is not None:
        st.write(data)
    #     st.pyplot(data)
elif model == 'KNN':
    data = request_data(ep.KNN)
    if data is not None:
        st.write(data)
    #     st.pyplot(data)
else:
    data = request_data(ep.TREE)
    if data is not None:
        st.write(data)
    #     st.pyplot(data)
