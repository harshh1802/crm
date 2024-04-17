import streamlit as st
import pandas as pd
from datetime import datetime
import io
from db_func import get_all_clients , add_client , update_client , add_interaction , get_client_interactions , get_all_interactions


# Function to fetch clients for dropdown
def fetch_clients():
    client_dict = get_all_clients()
    return client_dict

st.title("Client Interactions")
client_dict = fetch_clients()
client_data = st.selectbox("Select Client to View Interactions", options=list(client_dict), index=0)

if client_data:
    client_id = client_data.split(':')[0].strip()
    interactions = get_client_interactions(client_id)
    # df = pd.DataFrame(interactions, columns=['Date', 'Description', 'Follow-Up Date', 'Interested'])
    df = pd.DataFrame(interactions)
    st.write(df)
