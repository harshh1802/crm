import streamlit as st
import pandas as pd
from datetime import datetime
import io
from db_func import get_all_clients , add_client , update_client , add_interaction , get_client_interactions , get_all_interactions


st.title("Dashboard")
with st.form("Dashboard Date Range", clear_on_submit=False):
    start_date = st.date_input('Start Date')
    end_date = st.date_input("End Date")
    submit = st.form_submit_button("Show Interactions")

if submit or not st.session_state.get('first_load', True):

    if end_date > start_date:
        data = get_all_interactions() #TODO : Write function to get all interaction and filter on date basis
        df = pd.DataFrame(data)

        df2 = df[(df['date'] >= str(start_date)) & (df['date'] <= str(end_date)) ]
        st.dataframe(df2)
        st.session_state['first_load'] = False

    else:
        st.error("Check Date Range")
