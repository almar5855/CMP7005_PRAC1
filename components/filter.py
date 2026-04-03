
import datetime
import streamlit as st
import backend_stub as bs

# TODO: This file needs to use the Faux-RESTful API before submission

def dataset_filter():

    with st.expander('Dataset Filter'):
        all_regions = bs.get_region_names()
        regions = st.multiselect('Region', all_regions)
        select_all = st.checkbox('Select all', value=[len(regions)==0])
        if select_all:
            regions = all_regions

        min_date = datetime.date(2013, 3, 1)
        max_date = datetime.date(2017, 2, 28)
        date_from = st.date_input("From date",
                        value=min_date,
                        min_value=min_date,
                        max_value=max_date,
                        format="YYYY.MM.DD",
        )
        date_to = st.date_input("From date",
                        value=max_date,
                        min_value=date_from,
                        max_value=max_date,
                        format="YYYY.MM.DD",
        )

    return regions, date_from, date_to

def component_filter(
    multivariate=False,
    name='Component Filter',
    key=None):

    components = bs.get_component_names()
    components = components.drop(['No', 'station'])

    with st.expander(name):

        if multivariate:
            return st.multiselect('Components', components)

        return st.selectbox('Component', components, key=key)
