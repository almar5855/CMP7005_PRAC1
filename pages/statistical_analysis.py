
import streamlit as st
from http import HTTPStatus
from plotting_backend_stub import PlottingAPI as api, Endpoint as ep
from components import nav
from components import filter as fc

def request_data(endpoint, regions, date_from, date_to, component=None, period=None):

    response = api.request(endpoint, regions, date_from, date_to, component, period)

    if response['status'] == HTTPStatus.OK:
        return response['data']

    with st.expander('Error'):
        st.write(f'An error was returned from the backend: {response['data']}')  

    return None

st.set_page_config(layout='wide')

selected = nav.render_navbar()
st.title('Statistical Analysis')

col1, col2 = st.columns(2)
with col1:
    regions, date_from, date_to = fc.dataset_filter()
    analysis = fc.analysis_filter()
    analysis_period = fc.analysis_period_filter()

with col2:
    # TODO: Make this switch on analysis type
    pollution_component_x = fc.component_filter(False, 'X-Axis Filter', 'x-axis-filter')
    pollution_component_y = fc.component_filter(False, 'Y-Axis Filter', 'y-axis-filter')
    pollution_component = [pollution_component_x, pollution_component_y]

active_filter = f'##### Data for  {', '.join(regions)} between {date_from} to {date_to}'

if analysis == 'Bivariate':
    st.subheader('Bivariate Statistical Analysis')
    st.markdown(f'{active_filter}')

    data = request_data(ep.SCAT, regions, date_from, date_to, pollution_component)
    if data is not None:
        st.pyplot(data)

elif analysis == 'Multivariate':
    st.subheader(f'Multivariate Statistical Analysis')
    st.markdown(f'{active_filter}')

    data = request_data(ep.CORR, regions, date_from, date_to)
    if data is not None:
        st.pyplot(data)

else:
    st.subheader('Univariate Statistical Analysis')
    st.markdown(f'{active_filter}')

    st.subheader('Overview')

    left, right = st.columns(2)
    with left:

        data = request_data(ep.OVERVIEW, regions, date_from, date_to, pollution_component[0], analysis_period)
        if data is not None:
            st.pyplot(data)

    with right:

        data = request_data(ep.SEASONAL, regions, date_from, date_to, pollution_component[0], analysis_period)
        if data is not None:
            st.pyplot(data)


    st.subheader('Autocorrelation')
    data = request_data(ep.AUTO, regions, date_from, date_to, pollution_component[0])
    if data is not None:
        st.pyplot(data)



