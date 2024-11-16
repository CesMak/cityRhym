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
    if st.button("Generate Poem"):
        address = f"{first_name}, {last_name}, {postcode}, {street}, {house_number}, {city} "
        response = requests.post("http://localhost:5000/generate_poem", json={"address": address})
        poem = response.json()["poem"]
        st.write(poem)

if __name__ == "__main__":
    main()