from flask import Flask, request, jsonify
from api import promptLLM
from poemCheck import check_cross_rhyme
import requests  # For calling the language model API
import db        # importing the database python file
from random import randrange
app = Flask(__name__)

PROMT_EN      = "Create a funny poem with a cross rhyme about the eating and drinking habits in"
PROMPT_DE     = "Erstelle ein lustiges Gedicht im Kreuzreim über die Essens und Triinkgewohnheiten in"
REPORMPT_EN   = "This was a couplet rhyme. Please rearrange the words such that the middle words rhyme! Only return the poem!"
DEBUG_MESSAGE = ""

def storeAddress(first_name, last_name, street, house_number, zipcode, city):
    global DEBUG_MESSAGE
    DEBUG_MESSAGE += "I try to store this address: "+str(request.json["address"])+"\n"
    conn = db.create_connection("addresses")
    db.insert_address(conn, first_name, last_name, street, house_number, zipcode, city)
    conn.close()

def checkPoem(zipcode, city):
    global DEBUG_MESSAGE
    DEBUG_MESSAGE += "I will check if a poem exists for your zipcode:"+str(zipcode)+"\n"
    conn = db.create_connection("poem")
    poem = db.get_poem_by_zipcode(conn, zipcode)
    if poem is not None:
        DEBUG_MESSAGE += "A poem for your zipcode:" + str(zipcode) + " already exists"+"\n"
    else:
        DEBUG_MESSAGE += "A poem for your zipcode: " + str(zipcode) + " does not exist. I generate one now"+"\n"
        poem = promptLLM(prompt=PROMT_EN+city, reprompt=REPORMPT_EN)
        DEBUG_MESSAGE += "Cross rhyme check:\n"
        DEBUG_MESSAGE += check_cross_rhyme(poem)
        db.insert_poem(conn, zipcode, poem)
    conn.close()
    return poem

# API endpoint to handle address input and poem generation
@app.route('/generate_poem', methods=['POST'])
def generate_poem_endpoint():
    first_name, last_name, zipcode, street, house_number, city = request.json["address"].split(",")
    storeAddress(first_name, last_name, street, house_number, zipcode, city)
    poem = checkPoem(zipcode, city)
    return jsonify({'poem': poem, "debug_msg": DEBUG_MESSAGE})

if __name__ == '__main__':
    app.run(debug=True)