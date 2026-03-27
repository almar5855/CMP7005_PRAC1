
import streamlit as st
from http import HTTPStatus
from backend_stub import DatasetAPI as api, Endpoint as ep
from components import nav
from components import filter as fc

st.set_page_config(layout='wide')

selected = nav.render_navbar()
st.title(selected)
