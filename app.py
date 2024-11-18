import streamlit as st
import requests
import os

def main():
    DEBUG_MESSAGE = "System messages are displayed here"

    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    st.session_state.language = st.checkbox('Deutsch')
    if st.session_state.language:
        st.title('Reim Automat')
    else:
        st.title('Poem Generator')


    st.header("Create or edit an address or poem")
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name", value="Markus")
        street = st.text_input("Street", value="Bodensteinstr.")
        zipcode = st.text_input("zipcode", value="10117")

    # Add input fields to the second column
    with col2:
        last_name = st.text_input("Last Name", value="Lamprecht")
        house_number = st.text_input("House Number", value="12")
        city = st.text_input("City", value="Berlin")

    poem_input = st.empty()
    poem_input.text_area("Enter or modify a poem here", "Optional if you click generate for your zipcode a poem will be crated!")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate poem"):
            DEBUG_MESSAGE = "Try to generate a poem\n"
            address  = f"{first_name}, {last_name}, {zipcode}, {street}, {house_number}, {city} "
            response = requests.post("http://localhost:5000/generate_poem", json={"address": address, "language_de": st.session_state.language})
            poem     = ""
            if "poem" in response.json():
                poem = response.json()["poem"]
            else:
                DEBUG_MESSAGE += "Something went wrong in the back-end when generating your poem!"
            if "debug_msg" in response.json():
                DEBUG_MESSAGE += response.json()["debug_msg"]
            else:
                DEBUG_MESSAGE += "Error no debug messages from back-end."               
            poem = poem.replace("<br>","\n")
            poem_input.text_area("Enter or modify a poem here", value=str(poem))
    with col2:
        if st.button("Update location settings"):
            DEBUG_MESSAGE = "Try to update the location settings of "+first_name+","+last_name+"\n"
            address  = f"{first_name}, {last_name}, {zipcode}, {street}, {house_number}, {city} "
            response = requests.post("http://localhost:5000/update_location", json={"address": address})
            if "debug_msg" in response.json():
                DEBUG_MESSAGE += response.json()["debug_msg"]
            else:
                DEBUG_MESSAGE += "Error no debug messages from back-end."     
    ## Delete
    st.header("Delete an address")
    col11, col222, col333 = st.columns(3)
    with col11:
        first_name_to_delete = st.text_input("First Name", key="first_name_to_delete")
    with col222:
        last_name_to_delete = st.text_input("Last Name", key="last_name_to_delete")
    with col333:
        if st.button("Delete Address", key="delete_address"):
            DEBUG_MESSAGE = "Try to delete"+first_name+","+last_name+" from the database:"+"\n"
            response = requests.post("http://localhost:5000/delete_address", json={"first_name": first_name_to_delete, "last_name":last_name_to_delete})
            if "debug_msg" in response.json():
                DEBUG_MESSAGE += response.json()["debug_msg"]
            else:
                DEBUG_MESSAGE += "something went wrong in the connection to the db"
    st.header("Delete a poem")
    col11, col222 = st.columns(2)
    with col11:
        zipcode_to_delete_poem = st.text_input("Zipcode or City", key="zipcode_to_delete_poem")
    with col222:
        if st.button("Delete Poem", key="delete_poem"):
            DEBUG_MESSAGE = "Try to delete the poem of  "+zipcode_to_delete_poem+" from the database:"+"\n"
            response = requests.post("http://localhost:5000/delete_poem", json={"zip_or_city": zipcode_to_delete_poem, })
            if "debug_msg" in response.json():
                DEBUG_MESSAGE += response.json()["debug_msg"]
            else:
                DEBUG_MESSAGE += "something went wrong in the connection to the db"
    ## Show Database
    st.header("Show the database")
    col11, col222, coll333 = st.columns(3)
    with col11:
        if st.button("Show all addresses"):
            DEBUG_MESSAGE = "Show all addresses:\n"
            response = requests.post("http://localhost:5000/show_addresses", json={})
            if "addresses" in response.json():
                 if len(response.json()["addresses"])>0:
                    DEBUG_MESSAGE += response.json()["addresses"]+"\n"
                 else:
                    DEBUG_MESSAGE += "Addresses database is empty!"
            else:
                DEBUG_MESSAGE += "cannot show addresses the database is empty"
    with col222:
        if st.button("Show all poems"):
            DEBUG_MESSAGE = "Show all poems:\n"
            response = requests.post("http://localhost:5000/show_poems", json={})
            if "poems" in response.json():
                 if len(response.json()["poems"])>0:
                    DEBUG_MESSAGE += response.json()["poems"]+"\n"
                 else:
                    DEBUG_MESSAGE += "Poems database is empty!"
            else:
                DEBUG_MESSAGE += "cannot show poems the database is empty"
    
    #Delete all
    with coll333:
        if st.button("Delete whole database"):
            DEBUG_MESSAGE = "Delete whole database:\n"
            if os.path.exists("poem"):
                os.remove("poem")
                DEBUG_MESSAGE += "... deleted poems database\n"
            else:
                DEBUG_MESSAGE += "Cannot delete poems database -> its empty!\n"
            if os.path.exists("addresses"):
                os.remove("addresses")
                DEBUG_MESSAGE += "... deleted addresses database\n"
            else:
                DEBUG_MESSAGE += "Cannot delete addresses database -> its empty!\n"

    # System msgs
    st.text_area("System messages:", value=DEBUG_MESSAGE)
    DEBUG_MESSAGE = ""
if __name__ == "__main__":
    main()