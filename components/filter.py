
import datetime
import streamlit as st
import backend_stub as bs

def render_filter():

    with st.expander('Filter'):
        all_regions = bs.get_region_names()
        regions = st.multiselect('Region', all_regions)
        select_all = st.checkbox('Select all')
        if select_all:
            regions = all_regions
        #st.write(regions)

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
        # st.write(date_from)
        # st.write(date_to)

    return regions, date_from, date_to
