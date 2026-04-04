
from enum import Enum
import streamlit as st
from streamlit_option_menu import option_menu

OPTIONS = [
'Home',
'Dataset Information',
'Initial Observations',
'Data Preprocessing',
'Statistical Analysis',
'Modeling',
]

ROUTES = {
'Home': 'app.py',
'Dataset Information': 'pages/dataset_information.py',
'Initial Observations': 'pages/initial_observations.py',
'Data Preprocessing': 'pages/data_preprocessing.py',
'Statistical Analysis': 'pages/statistical_analysis.py',
'Modeling': 'pages/model.py',
}

def switch_page(selected: str) -> None:

    if 'current_page' not in st.session_state:
        st.session_state.current_page = selected

    if selected != st.session_state.current_page:

        st.session_state.current_page = selected

        st.switch_page(ROUTES[selected])


def render_navbar() -> str:

    selected = 0
    if 'current_page' in st.session_state:
        selected = OPTIONS.index(st.session_state.current_page)

    with st.sidebar:
        selected = option_menu(
            menu_title='Navigation',
            #options=['Home', 'Dataset Information', 'Initial Observations', 'Data Preprocessing', 'Statistical Analysis', 'Modeling'],
            options=OPTIONS,
            icons=['house', 'list-task', 'graph-up', 'gear', 'graph-up', 'gear'],
            menu_icon="cast",
            #default_index=0,
            manual_select=selected
        )

    switch_page(selected)

    return selected
