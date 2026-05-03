
import streamlit as st
from streamlit_option_menu import option_menu

OPTIONS = [
'Home',
'Dataset Information',
'Initial Observations',
'Statistical Analysis',
'Modeling',
]

ROUTES = {
'Home': 'app.py',
'Dataset Information': 'pages/dataset_information.py',
'Initial Observations': 'pages/initial_observations.py',
'Statistical Analysis': 'pages/statistical_analysis.py',
'Modeling': 'pages/model.py',
}

def switch_page(selected: str) -> None:

    st.switch_page(ROUTES[selected])


def render_navbar(current_page: str) -> None:

    default_selection = OPTIONS.index(current_page)

    with st.sidebar:
        selected = option_menu(
            menu_title='Navigation',
            options=OPTIONS,
            icons=['house', 'list-task', 'graph-up', 'graph-up', 'gear'],
            menu_icon="cast",
            default_index=default_selection,
        )

    if current_page != selected:
        switch_page(selected)

    return selected
