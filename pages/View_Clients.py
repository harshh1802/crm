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