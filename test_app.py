
import streamlit as st
from streamlit_option_menu import option_menu
import backend_stub as bs
import datetime

with st.sidebar:
    selected = option_menu(
        menu_title='Navigation',
        options=['Home', 'Dataset Understanding', 'Data Preprocessing', 'Statisitical Analysis', 'Modeling'],
        icons=['house', 'list-task', 'gear', 'graph-up', 'gear'],
        menu_icon="cast",
        default_index=0,
    )
st.title(f'{selected}')

def refresh_dataset(regions=None, date_from=None, date_to=None):
    st.dataframe(bs.get_data(regions, date_from, date_to))

all_regions = bs.get_region_names()
regions = st.multiselect('Region', all_regions)
select_all = st.checkbox('Select all')
if select_all:
    regions = all_regions
st.write(regions)

min_date = datetime.date(2013, 3, 1)
max_date = datetime.date(2017, 2, 28)
date_from = st.date_input("From date",
                value=min_date,
                min_value=min_date,
                max_value=max_date,
                format="YYYY.MM.DD",
                on_change=refresh_dataset,
)
date_to = st.date_input("From date",
                value=max_date,
                min_value=date_from,
                max_value=max_date,
                format="YYYY.MM.DD",
                on_change=refresh_dataset,
)
st.write(date_from)
st.write(date_to)
refresh_dataset(regions, date_from, date_to)

