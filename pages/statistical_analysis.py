
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
        st.write(f"An error was returned from the backend: {response['data']}")

    return None

st.set_page_config(layout='wide')

selected = nav.render_navbar()

with st.sidebar:
    st.markdown('#### Filters')

    regions, date_from, date_to = fc.dataset_filter()
    analysis = fc.analysis_filter()
    analysis_period = fc.analysis_period_filter()

    pollution_component=None
    if analysis == 'Univariate':
        pollution_component = fc.component_filter(False, 'X-Axis Filter', 'x-axis-filter')
    if analysis == 'Bivariate':
        pollution_component_x = fc.component_filter(False, 'X-Axis Filter', 'x-axis-filter')
        pollution_component_y = fc.component_filter(False, 'Y-Axis Filter', 'y-axis-filter', 1)
        pollution_component = [pollution_component_x, pollution_component_y]

st.title('Statistical Analysis')
st.text("Explore the univariate, bivariate, and multivariate relationships in the dataset")

display_components = pollution_component
if analysis == 'Multivariate':
    display_components = 'All'

active_filter = f'##### Visualising {display_components} data for  {', '.join(regions)} between {date_from} to {date_to}'

if analysis == 'Bivariate':
    st.subheader('Bivariate Statistical Analysis')
    st.markdown(f'{active_filter}')

    with st.container(border=True):
        data = request_data(ep.SCAT, regions, date_from, date_to, pollution_component)
        if data is not None:
            st.pyplot(data)

elif analysis == 'Multivariate':
    st.subheader(f'Multivariate Statistical Analysis')
    st.markdown(f'{active_filter}')

    with st.container(border=True):
        data = request_data(ep.CORR, regions, date_from, date_to)
        if data is not None:
            st.pyplot(data)

else:
    st.subheader('Univariate Statistical Analysis')
    st.markdown(f'{active_filter}')

    st.subheader('Overview')

    left, right = st.columns(2, gap ="large")
    with left:
        with st.container(border=True):
            data = request_data(ep.OVERVIEW, regions, date_from, date_to, pollution_component, analysis_period)
            if data is not None:
                st.pyplot(data)

    with right:
        with st.container(border=True):
            data = request_data(ep.SEASONAL, regions, date_from, date_to, pollution_component, analysis_period)
            if data is not None:
                st.pyplot(data)

    st.divider()

    with st.container(border=True):
        st.subheader('Autocorrelation')
        data = request_data(ep.AUTO, regions, date_from, date_to, pollution_component)
        if data is not None:
            st.pyplot(data)



