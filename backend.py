from flask import Flask, request, jsonify
from api import promptLLM
import requests  # For calling the language model API
import db        # importing the database python file
from random import randrange
app = Flask(__name__)

PROMT_EN = "Create a funny poem with a cross rhyme about the eating and drinking habits in"
PROMPT_DE= "Erstelle ein lustiges Gedicht im Kreuzreim über die Essens und Triinkgewohnheiten in"
REPORMPT_EN = "This was a couplet rhyme. Please rearrange the words such that the middle words rhyme! Only return the poem!"

def storeAddress(first_name, last_name, postcode, street, house_number, city ):
    print("I try to store this address:", request.json["address"].split(","))
    conn = db.create_connection("addresses")
    db.insert_address(conn, first_name, last_name, street, house_number, postcode, city)
    db.print_table_entries(conn, "addresses" )
    conn.close()

def checkPoem(postcode, city):
    print("I will check if a poem exists for your postcode:", postcode)
    conn = db.create_connection("poem")
    poem = db.get_poem_by_postcode(conn, postcode)
    if poem is not None:
        print("A poem for your postcode:",postcode," already exists")
    else:
        print("A poem for your postcode:",postcode," does NOT exist. I generate one now:")
        poem = promptLLM(prompt=PROMT_EN+city, reprompt=REPORMPT_EN)
        db.insert_poem(conn, postcode, poem)
    #db.print_table_entries(conn, "poem")
    conn.close()
    return poem

# API endpoint to handle address input and poem generation
@app.route('/generate_poem', methods=['POST'])
def generate_poem_endpoint():
    first_name, last_name, postcode, street, house_number, city = request.json["address"].split(",")
    storeAddress(first_name, last_name, postcode, street, house_number, city )
    poem = checkPoem(postcode, city)
    return jsonify({'poem': poem})

if __name__ == '__main__':
    app.run(debug=True)