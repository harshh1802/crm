import streamlit as st
import pandas as pd
from datetime import datetime
import io
from db_func import get_all_clients , add_client , update_client , add_interaction , get_client_interactions , get_all_interactions




def fetch_clients():
    client_dict = get_all_clients()
    return client_dict


st.title("Log Client Interaction")
client_dict = fetch_clients()
client_data = st.selectbox("Select Client", options=list(client_dict), index=0)

if client_data:
    with st.form("Log Interaction Form", clear_on_submit=True):
        interaction_type = st.selectbox("Interaction Type" , options=['Call' , 'Mail'])
        interaction_date = st.date_input("Interaction Date", datetime.now())
        description = st.text_area("Description")
        is_follow_up = st.checkbox("Follow Up")
        follow_up_date = st.date_input("Follow-Up Date")
        interested = st.checkbox("Interested")
        submit = st.form_submit_button("Log Interaction")
            
        if submit:

            if (is_follow_up == True ) and (follow_up_date < interaction_date):
                st.error("Check Follow up date")

            else:
                client_id = client_data.split(':')[0].strip()
                client_name = client_data.split(':')[1].split('-')[0].strip()
                company_name = client_data.split('-')[1].split('(')[0].strip()
                
                add_interaction(client_id,
                                client_name,
                                company_name,
                                str(interaction_date),
                                interaction_type,
                                description,
                                str(follow_up_date)
                                    )
                    
                st.success("Interaction Logged Successfully!")