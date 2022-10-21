from quart import Quart, request, jsonify, abort
from quart_schema import QuartSchema #, DataSource, validate_request
import sqlalchemy
from sqlalchemy import create_engine, insert, select, Table, Column, Integer, String, Boolean
from databases import Database
import socket
from dataclasses import dataclass
import json
import wget
import sqlite3
import correctWords



db = Database('sqlite:////home/student/Documents/449-wordle/wordle-DB')



app = Quart(__name__)
QuartSchema(app)


@app.errorhandler(404)
def not_found(e):
    return {"error": "The resource could not be found"}, 404

@app.route("/")
async def index():
    return "hello"


@app.route("/register", methods=["POST"])
async def create_user():
    data = await request.get_json()

    user_data = f"{data['user_id']} {data['password']}"
    app.logger.debug(user_data)
    
    entered_id = data['user_id']
    entered_pass = data['password']
    
    query = "INSERT INTO users(user_id, password) VALUES (:user_id, :password)"
  

    values = {"user_id": entered_id, "password": entered_pass}
    await db.execute(query=query, values=values)

    return jsonify({"authenticated": "true"})


@app.route("/login", methods=["POST"])
async def login():
    data = await request.get_json()
    user_data = f"{data['user_id']} {data['password']}"

    app.logger.debug(user_data)
    entered_id = data['user_id']
    entered_pass = data['password']
    
    query = "SELECT * FROM users WHERE user_id = :id and password = :password"
    row = await db.execute(query=query, values={"id": entered_id, "password": entered_pass})
    if row:
    	return jsonify({"authenticated": "true"})
    

    

@app.route("/login/<int:id><string:password>", methods=["GET"])
async def login_user(id, password):
    db = await request.get_json()
    book = await db.fetch_one("SELECT * FROM users WHERE user_id = :user_id AND password = :password", values={"user_id": id, "password": password})
    if book:
        return jsonify({"authenticated": "true"})
    else:
        abort(404)

@app.route("/create_new_game/<int:id>", methods=["POST"])
async def create_new_game(id):
    query = "INSERT INTO games (game_id, game_secret_word, won, number_of_guesses_made, number_of_guesses_left, user_id) VALUES (NULL, :word, :won, :made, :left, :user_id)"
    await db.execute(query=query, values={"word": "word", "won": False, "made": 0, "left": 6, "user_id": id})
    return jsonify({"Success": "New Game Entered"})





@app.route("/TEST_word_load/", methods=["POST"])
async def word_load():

    #for word in correctWord:
    for word in correctWords.correctWord:
        query = "INSERT INTO correctWords (correct_word_id, correct_word, game_id) VALUES (NULL, :correctWord, NULL)"
        await db.execute(query=query,
                         values={"correctWord": word})

    return "All words loaded into DB"



@app.route('/input/', methods=['GET'])
async def input():
    #randomly selecting a word from the correctWords.py
    secretWord = str(random.choice(correctWords.correctWord))
    #parsing the secretWord into single char
    firstLetterSW = secretWord[0]
    secondLetterSW = secretWord[1]
    thirdLetterSW = secretWord[2]
    fourthLetterSW = secretWord[3]
    fifthLetterSW = secretWord[4]

    word = str (request.args.get('word'))
    counter = 0
    
    if word == "secret":
        return {
                'Call' : 'Input',
                'Status' : 200,
                'Response' : secretWord
                }, 200
    
    if word == "":
        return {
                'Call' : 'Input',
                'Status' : 400,
                'Response' : 'No Word Input'
                }, 400
    
    if len(word) != 5:
        return {
                'Call' : 'Input',
                'Status' : 400,
                'Response' : 'Is not length 5'
                }, 400

    if word in correctWords.correctWord:
        return {
                'Call' : 'Input',
                'Status' : 200,
                'Response' : 'Valid word but not Secret Word'
                }, 200

    if word == secretWord:
        return {
                'Call' : 'Input',
                'Status' : 200,
                'Response' : True
                }, 200



@app.route("/DB")
async def db_connect():

    connection = await db.connect()
    print("connection: " + str(connection))
    return str(connection)

app.run(host='0.0.0.0', port=5000)

