
import streamlit as st
import backend_stub as bs
from components import nav
from components import filter as fc

selected = nav.render_navbar()
st.title('Modeling')

#regions, date_from, date_to = fc.dataset_filter()

st.set_page_config(layout='wide')

col1, col2 = st.columns(2)
with col1:
    model = fc.model_filter()
with col2:
    component = fc.component_filter(False, 'Independent Variable', 'TBD')

#with col2:
#    pollution_component = fc.component_filter(False)
