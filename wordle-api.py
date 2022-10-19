from quart import Quart, request, jsonify, abort
from quart_schema import QuartSchema #, DataSource, validate_request
import sqlalchemy
from sqlalchemy import create_engine, insert, select, Table, Column, Integer, String, Boolean
from databases import Database
import socket
from dataclasses import dataclass
from flask import render_template, abort



engine = create_engine('sqlite:///C:/Users/bruht/PycharmProjects/quart-test/testDB.db', echo=True)
db = Database('sqlite:///C:/Users/bruht/PycharmProjects/quart-test/testDB.db')
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("password", String(length=100)),
    Column("games_played", Integer)
)


games = sqlalchemy.Table(
    "games",
    metadata,
    Column("game_id", Integer, primary_key=True),
    Column("game_secret_word", String(length=100)),
    Column("won", Boolean),
    Column("number_of_guesses_made", Integer),
    Column("number_of_guesses_left", Integer),
    Column("user_id", Integer, foreign_key=True)
)


wordGuess = sqlalchemy.Table(
    "wordGuess",
    metadata,
    Column("user_word_guess_id", Integer, primary_key=True),
    Column("user_word_guess", String(length=100)),
    Column("game_id", Integer, foreign_key=True)
)

metadata.create_all(engine)


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

    query = users.insert()
    values = {"user_id": entered_id, "password": entered_pass}
    await db.execute(query=query, values=values)

    isAuthenticated = True

    return jsonify({"authenticated": "true"})


@app.route("/login", methods=["POST"])
async def login():
    data = await request.get_json()

    user_data = f"{data['user_id']} {data['password']}"
    app.logger.debug(user_data)
    entered_id = data['user_id']
    entered_pass = data['password']

    query = "SELECT * FROM users WHERE user_id = :id AND password = :pass;"
    row = await db.fetch_one(query=query, values={"id": entered_id, "pass": entered_pass})
    if row is not None:
        return jsonify({"authenticated": "true"})
    else:
        abort(404)


@app.route("/create_new_game/<int:id>", methods=["POST"])
async def create_new_game(id):

    lastGameIDQuery = "SELECT game_id FROM games ORDER BY game_id DESC LIMIT 1;"
    lastRow = await db.fetch_one(query=lastGameIDQuery)
    if lastRow is not None:
        for game_id in lastRow:
            new_game_id = game_id + 1
            print("new_game_id: " + str(new_game_id))
            query = "INSERT INTO games (game_id, game_secret_word, won, number_of_guesses_made, number_of_guesses_left, user_id) VALUES (:newID, :word, :won, :made, :left, :user_id)"
            await db.execute(query=query, values={"newID": new_game_id, "word": "word", "won": False, "made": 0, "left": 6, "user_id": id})
            return "New Game Entered"
    else:
        query = "INSERT INTO games (game_id, user_id) VALUES (1, :user_id);"
        await db.execute(query=query, values={"user_id": id})
        return "First Game Entered"




@app.route("/DB")
async def db_connect():

    connection = await db.connect()
    print("connection: " + str(connection))
    return str(connection)

app.run()

