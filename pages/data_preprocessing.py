
import streamlit as st
import backend_stub as bs
from components import nav
from components import filter as fc

selected = nav.render_navbar()
st.title(selected)
regions, date_from, date_to = fc.dataset_filter()
