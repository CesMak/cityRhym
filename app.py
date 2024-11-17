import streamlit as st
import requests

def main():
    st.title("Poem Generator")

    # Input fields for address
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    street = st.text_input("Street")
    house_number = st.text_input("House Number")
    postcode = st.text_input("Postcode")
    city = st.text_input("City")


    # Button to trigger poem generation
    if st.button("Generate poem"):
        address = f"{first_name}, {last_name}, {postcode}, {street}, {house_number}, {city} "
        response = requests.post("http://localhost:5000/generate_poem", json={"address": address})
        poem = response.json()["poem"]
        print("Frontend:::")
        print(poem)
        poem = poem.replace("\n","<br>")
        st.write(poem, unsafe_allow_html=True)

    # if st.button("Save Poem and address"):
    #     print("huhu")
    
    # if st.button("Delete poem"):
    #     print("hihi")

    # if st.button("Delete address"):
    #     print("jaaj")

if __name__ == "__main__":
    main()