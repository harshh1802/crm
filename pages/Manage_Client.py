elif app_mode == "Manage Clients":
    st.title("Manage Client Information")
    client_dict = fetch_clients()
    client_data = st.selectbox("Select Client", options=list(client_dict), index=0)

    if client_data:
        client_id = client_data.split(':')[0].strip()
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
