import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import io

# Initialize connection to your personal database
conn = sqlite3.connect('crm.db', check_same_thread=False)

# Function to run queries
def run_query(query, params=()):
    with conn:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        return cur.fetchall()

# Create tables if they don't exist
def create_tables():
    queries = [
        """
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone TEXT,
            company TEXT,
            designation TEXT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY,
            client_id INTEGER,
            interaction_date DATE,
            description TEXT,
            follow_up_date DATE,
            interested BOOLEAN,
            FOREIGN KEY (client_id) REFERENCES clients (id)
        );
        """
    ]
    for query in queries:
        run_query(query)

create_tables()

# Sidebar for navigation
st.sidebar.title("CRM Navigation")
app_mode = st.sidebar.selectbox("Choose the app mode",
    ["Add Client", "Log Interaction", "View Interactions", "Dashboard","Manage Clients","View Clients"])

# Function to fetch clients for dropdown
def fetch_clients():
    query = "SELECT id, first_name, last_name, company, designation FROM clients;"
    clients = run_query(query)
    client_dict = {
        f"{id}: {first_name} {last_name} - {company} ({designation})": id
        for id, first_name, last_name, company, designation in clients
    }
    return client_dict

if app_mode == "Add Client":
    st.title("Add New Client")
    with st.form("Add Client Form", clear_on_submit=False):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        company = st.text_input("Company")
        designation = st.text_input("Designation")
        submit_individual = st.form_submit_button("Add Individual Client")
        
        if submit_individual:
            query = "INSERT INTO clients (first_name, last_name, email, phone, company, designation) VALUES (?, ?, ?, ?, ?, ?);"
            run_query(query, (first_name, last_name, email, phone, company, designation))
            st.success("Client Added Successfully!")
    
    st.write("---")  # Add a visual separator
    st.header("Bulk Upload Client Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        data = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
        df = pd.read_csv(data)

        with st.spinner("Uploading data..."):
            for _, row in df.iterrows():
                query = "INSERT INTO clients (first_name, last_name, email, phone, company, designation) VALUES (?, ?, ?, ?, ?, ?);"
                run_query(query, (row['fname'], row['lname'], row['email'], row['contact'], row['company'], row.get('designation', '')))
            st.success("All clients added successfully!")

elif app_mode == "Log Interaction":
    st.title("Log Client Interaction")
    client_dict = fetch_clients()
    client_name = st.selectbox("Select Client", options=list(client_dict.keys()), index=0)

    if client_name:
        with st.form("Log Interaction Form", clear_on_submit=True):
            interaction_date = st.date_input("Interaction Date", datetime.now())
            description = st.text_area("Description")
            follow_up_date = st.date_input("Follow-Up Date")
            interested = st.checkbox("Interested")
            submit = st.form_submit_button("Log Interaction")
            
            if submit:
                client_id = client_dict[client_name]
                query = "INSERT INTO interactions (client_id, interaction_date, description, follow_up_date, interested) VALUES (?, ?, ?, ?, ?);"
                run_query(query, (client_id, interaction_date, description, follow_up_date, interested))
                st.success("Interaction Logged Successfully!")

elif app_mode == "View Interactions":
    st.title("Client Interactions")
    client_dict = fetch_clients()
    client_name = st.selectbox("Select Client to View Interactions", options=list(client_dict.keys()), index=0)

    if client_name:
        client_id = client_dict[client_name]
        query = "SELECT interaction_date, description, follow_up_date, interested FROM interactions WHERE client_id = ? ORDER BY interaction_date DESC;"
        interactions = run_query(query, (client_id,))
        df = pd.DataFrame(interactions, columns=['Date', 'Description', 'Follow-Up Date', 'Interested'])
        st.write(df)

elif app_mode == "Dashboard":
    st.title("Dashboard")
    with st.form("Dashboard Date Range", clear_on_submit=False):
        start_date, end_date = st.select_slider(
            "Select a date range",
            options=pd.date_range(datetime.today().replace(day=1), periods=12, freq='M').tolist(),
            value=(datetime.today().replace(day=1), datetime.today())
        )
        submit = st.form_submit_button("Show Interactions")
    
    if submit or not st.session_state.get('first_load', True):
        query = """
        SELECT interaction_date, description, follow_up_date, interested
        FROM interactions
        WHERE interaction_date BETWEEN ? AND ?
        ORDER BY interaction_date;
        """
        data = run_query(query, (start_date, end_date))
        df = pd.DataFrame(data, columns=['Interaction Date', 'Description', 'Follow-Up Date', 'Interested'])
        st.dataframe(df)
        st.session_state['first_load'] = False

elif app_mode == "Manage Clients":
    st.title("Manage Client Information")
    client_dict = fetch_clients()
    client_name = st.selectbox("Select Client", options=list(client_dict.keys()), index=0)

    if client_name:
        client_id = client_dict[client_name]
        query = "SELECT first_name, last_name, email, phone, company, designation FROM clients WHERE id = ?;"
        client_data = run_query(query, (client_id,))[0]  # Fetch existing data for the selected client
        
        with st.form("Client Management Form", clear_on_submit=False):
            first_name = st.text_input("First Name", value=client_data[0])
            last_name = st.text_input("Last Name", value=client_data[1])
            email = st.text_input("Email", value=client_data[2])
            phone = st.text_input("Phone", value=client_data[3])
            company = st.text_input("Company", value=client_data[4])
            designation = st.text_input("Designation", value=client_data[5])
            
            col1, col2 = st.columns(2)
            with col1:
                submit_update = st.form_submit_button("Update Client")
            with col2:
                delete_client = st.form_submit_button("Delete Client")
            
            if submit_update:
                update_query = """
                UPDATE clients
                SET first_name = ?, last_name = ?, email = ?, phone = ?, company = ?, designation = ?
                WHERE id = ?;
                """
                run_query(update_query, (first_name, last_name, email, phone, company, designation, client_id))
                st.success("Client Updated Successfully!")
                
            if delete_client:
                delete_query = "DELETE FROM clients WHERE id = ?;"
                run_query(delete_query, (client_id,))
                st.success(f"Client '{client_name}' Deleted Successfully!")
                # Refresh or redirect to avoid further actions on a deleted client
                st.experimental_rerun()


elif app_mode == "View Clients":
    st.title("Client Overview")

    # Fetch all clients from the database
    query = "SELECT id, first_name || ' ' || last_name AS name, email, phone, company, designation FROM clients;"
    clients_data = run_query(query)
    df_clients = pd.DataFrame(clients_data, columns=['ID', 'Name', 'Email', 'Phone', 'Company', 'Designation'])

    # Temporary workaround to include buttons in a DataFrame display
    # This adds a column with "Add Interaction" buttons for each client
    df_clients['Add Interaction'] = df_clients['ID'].apply(lambda x: f"Add Interaction {x}")

    st.dataframe(df_clients.drop(columns=['ID']))  # Hide the ID column from display

    # Detect button clicks in the "Add Interaction" column
    interaction_client_id = st.text_input("Enter Client ID to Add Interaction", "")
    if interaction_client_id:
        # Convert input to integer
        try:
            interaction_client_id = int(interaction_client_id.split()[-1])  # Extract ID from button text
            # Verify if the client ID exists in the database
            if interaction_client_id in df_clients['ID'].values:
                st.write(f"Add Interaction for Client ID: {interaction_client_id}")
                # Interaction form (simplified version)
                with st.form(f"Interaction_{interaction_client_id}", clear_on_submit=True):
                    interaction_date = st.date_input("Interaction Date", datetime.now())
                    description = st.text_area("Description")
                    follow_up_date = st.date_input("Follow-Up Date")
                    interested = st.checkbox("Interested")
                    submit_interaction = st.form_submit_button("Log Interaction")
                    
                    if submit_interaction:
                        # SQL query to insert the new interaction
                        query = """
                        INSERT INTO interactions (client_id, interaction_date, description, follow_up_date, interested)
                        VALUES (?, ?, ?, ?, ?);
                        """
                        run_query(query, (interaction_client_id, interaction_date, description, follow_up_date, interested))
                        st.success(f"Interaction added for Client ID: {interaction_client_id}")
        except ValueError:
            st.error("Invalid Client ID. Please use the format 'Add Interaction ID'.")

