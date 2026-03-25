
import streamlit as st
import backend_stub as bs
from components import nav
from components import filter as fc

selected = nav.render_navbar()
st.title(selected)

regions, date_from, date_to = fc.render_filter()

st.write(bs.get_dataset_shape(regions, date_from, date_to))
st.write(bs.get_dataset_info(regions, date_from, date_to))
st.write(bs.get_dataset_description(regions, date_from, date_to))

