import streamlit as st
import pandas as pd
from datetime import datetime
import io
from db_func import get_all_clients , add_client , update_client , add_interaction , get_client_interactions , get_all_interactions



 # Add a visual separator
st.header("Bulk Upload Client Data")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    # data = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
    df = pd.read_csv(uploaded_file)

    if st.button('Upload'):

        with st.spinner("Uploading data..."):
            for _, row in df.iterrows():
                add_client(row['client_id'] , row['name'] , row['phone'] , row['mail'] , row['company'] , None , None)
            st.success("All clients added successfully!")

st.write("---") 

st.header("Add Individual Client")

with st.form("Add Client Form", clear_on_submit=False):
    client_id = st.text_input("client_id")
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    company = st.text_input("Company")
    designation = st.text_input("Designation")
    submit_individual = st.form_submit_button("Add Individual Client")
    
    if submit_individual:
        add_client(client_id , name , phone , email , company , designation , None)
        st.success("Client Added Successfully!")
