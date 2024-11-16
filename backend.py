from flask import Flask, request, jsonify
import requests  # For calling the language model API
import db        # importing the database python file
from random import randrange
app = Flask(__name__)

# Replace with your database connection details
# ...

# Function to generate a poem
def generate_poem(address):
    # Call the language model API with the address
    response = requests.post("language_model_api_endpoint", json={"address": address})
    poem = response.json()["poem"]
    return poem

def storeAddress(first_name, last_name, postcode, street, house_number, city ):
    print("I try to store this address:", request.json["address"].split(","))
    conn = db.create_connection("addresses")
    db.insert_address(conn, first_name, last_name, street, house_number, postcode, city)
    db.print_table_entries(conn, "addresses" )
    conn.close()

def checkPoem(postcode):
    print("I will check if a poem exists for your postcode:", postcode)
    conn = db.create_connection("poem")
    poem = ""
    if(db.check_if_poem_exists(conn, postcode)):
        print("A poem for your postcode:",postcode," already exists")
    else:
        print("A poem for your postcode:",postcode," does NOT exist. I generate one now:")
        poem="Poem text here......"+str(randrange(0,1000))
        db.insert_poem(conn, postcode, poem)
    db.print_table_entries(conn, "poem")
    conn.close()

# API endpoint to handle address input and poem generation
@app.route('/generate_poem', methods=['POST'])
def generate_poem_endpoint():
    first_name, last_name, postcode, street, house_number, city = request.json["address"].split(",")
    storeAddress(first_name, last_name, postcode, street, house_number, city )
    checkPoem(postcode)

    # TODO change from here:
    address = request.json['address']
    poem = "Huhu"+address #generate_poem(address)
    # Store the address and poem in the database
    # ...
    return jsonify({'poem': poem})

# ... (Other API endpoints for CRUD operations on addresses)

if __name__ == '__main__':
    app.run(debug=True)