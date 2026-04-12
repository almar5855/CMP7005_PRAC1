
import streamlit as st
from http import HTTPStatus
from plotting_backend_stub import PlottingAPI as api, Endpoint as ep
from components import nav
from components import filter as fc

# TODO: This needs to find one place to live
def request_data(endpoint, regions, date_from, date_to, component):

    response = api.request(endpoint, regions, date_from, date_to, component)

    if response['status'] == HTTPStatus.OK:
        return response['data']

    with st.expander('Error'):
        st.write(f'An error was returned from the backend: {response['data']}')  

    return None

st.set_page_config(layout='wide')

selected = nav.render_navbar()
st.title('Initial Observations')

col1, col2 = st.columns(2)
with col1:
    regions, date_from, date_to = fc.dataset_filter()

with col2:
    pollution_component = fc.component_filter(False)

st.markdown("---")

active_filter = f'##### Data for  {', '.join(regions)} between {date_from} to {date_to}'
st.markdown(active_filter)
st.markdown("---")

left, right = st.columns(2, gap="small")
with left:
    data = request_data(ep.HIST, regions, date_from, date_to, pollution_component)

    with st.container(height=500):

        st.markdown(f'##### Distribution of {pollution_component} concentrations')
        st.pyplot(data)

    st.markdown("---")

with right:

    data = request_data(ep.BOX, regions, date_from, date_to, pollution_component)

    with st.container(height=500):

        st.markdown(f'##### Boxplot of {pollution_component} concentrations')
        st.pyplot(data)

    st.markdown("---")
