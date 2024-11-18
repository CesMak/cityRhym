from flask import Flask, request, jsonify
from api import promptLLM
from poemCheck import check_cross_rhyme
import requests  # For calling the language model API
import db        # importing the database python file
from random import randrange
app = Flask(__name__)

PROMPT_EN     = "Create a funny poem with a cross rhyme about the eating and drinking habits in"
REPORMPT_EN   = "This was a couplet rhyme. Please rearrange the words such that the middle words rhyme! Only return the poem!"

PROMPT_DE     = "Erstelle ein lustiges Gedicht im Kreuzreim über die Essens und Triinkgewohnheiten in"
REPROMPT_DE   = "Das war ein Paarreim (AABB). Bitte gestalte den Reim zu einem Kreuzreim (ABAB) um. Gib nur den Reim  selbst zurück!"
DEBUG_MESSAGE = ""

def storeAddress(first_name, last_name, street, house_number, zipcode, city):
    global DEBUG_MESSAGE
    DEBUG_MESSAGE = "I try to store this address: "+str(request.json["address"])+"\n"
    conn = db.create_connection("addresses")
    db.insert_address(conn, first_name, last_name, street, house_number, zipcode, city)
    conn.close()

def checkPoem(zipcode, city, language_de):
    global DEBUG_MESSAGE
    DEBUG_MESSAGE = "I will check if a poem exists for your zipcode:"+str(zipcode)+"\n"
    conn = db.create_connection("poem")
    print(zipcode)
    print("poem exits:", db.check_if_poem_exists(conn,zipcode))
    poem = db.get_poem_by_zipcode(conn, zipcode)
    if poem is not None:
        DEBUG_MESSAGE += "A poem for your zipcode:" + str(zipcode) + " already exists"+"\n"
    else:
        DEBUG_MESSAGE += "A poem for your zipcode: " + str(zipcode) + " does not exist. I generate one now"+"\n"
        if language_de:
            poem = promptLLM(prompt=PROMPT_DE+city, reprompt=REPROMPT_DE)    
            DEBUG_MESSAGE += "Cross rhyme check is not possible due to lack of dictionary in nltk"
        else:
            poem = promptLLM(prompt=PROMPT_EN+city, reprompt=REPORMPT_EN)
            DEBUG_MESSAGE += "Cross rhyme check:\n"
            DEBUG_MESSAGE += check_cross_rhyme(poem)
        db.insert_poem(conn, zipcode, city, poem)
    conn.close()
    return poem

# API endpoint to handle address input and poem generation
@app.route('/generate_poem', methods=['POST'])
def generate_poem_endpoint():
    first_name, last_name, zipcode, street, house_number, city = request.json["address"].split(",")
    language_de = request.json["language_de"]
    storeAddress(first_name, last_name, street, house_number, zipcode, city)
    poem = checkPoem(zipcode, city, language_de)
    return jsonify({'poem': poem, "debug_msg": DEBUG_MESSAGE})

@app.route('/update_location', methods=['POST'])
def update_location():
    first_name, last_name, zipcode, street, house_number, city = request.json["address"].split(",")
    conn = db.create_connection("addresses")
    DEBUG_MESSAGE = db.update_location(conn, first_name, last_name, street, house_number, zipcode, city)
    return jsonify({"debug_msg": DEBUG_MESSAGE})

@app.route('/show_addresses', methods=['POST'])
def show_addresses():
    conn = db.create_connection("addresses")
    addresses = db.print_table_entries(conn, "addresses")
    return jsonify({'addresses': addresses})

@app.route('/show_poems', methods=['POST'])
def show_poems():
    conn = db.create_connection("poem")
    poems = db.print_table_entries(conn, "poem")
    return jsonify({'poems': poems})

@app.route('/delete_address', methods=['POST'])
def delete_address():
    first_name  = request.json["first_name"]
    last_name   = request.json["last_name"]
    conn = db.create_connection("addresses")
    DEBUG_MESSAGE = db.delete_address(conn, first_name, last_name)
    return jsonify({'debug_msg': DEBUG_MESSAGE})

@app.route('/delete_poem', methods=['POST'])
def delete_poem():
    zip_or_city  = request.json["zip_or_city"]
    conn = db.create_connection("poem")
    DEBUG_MESSAGE = db.delete_poem(conn, zip_or_city)
    return jsonify({'debug_msg': DEBUG_MESSAGE})

if __name__ == '__main__':
    app.run(debug=True)