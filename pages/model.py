
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
st.text("Select your modeling approach and observe the results from the classification task")
st.divider()

with st.sidebar:
    model = fc.model_filter()

st.subheader(f"Viewing results from the {model} classification model")
st.divider()

data = None

if model == 'Logistic Regression':
    data = request_data(ep.LINEAR)
elif model == 'KNN':
    data = request_data(ep.KNN)
else:
    data = request_data(ep.TREE)

if data is not None:

    left, right = st.columns(2, gap ="large")
    with left:
        st.subheader("Metrics")
        st.code(data[0])
    with right:
        st.subheader("Confusion Matrix")
        st.pyplot(data[1])
