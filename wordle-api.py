from quart import Quart, request, jsonify
from quart_schema import QuartSchema #, DataSource, validate_request
import sqlalchemy
from sqlalchemy import create_engine, insert, select, Table, Column, Integer, String
from databases import Database
import socket
from dataclasses import dataclass
from flask import render_template, abort


db = Database('sqlite:///C:/Users/bruht/PycharmProjects/quart-test/testDB.db')
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("password", String(length=100))
)


app = Quart(__name__)
QuartSchema(app)

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

    return jsonify({"Account created with ID": entered_id})


@app.route("/login", methods=["POST"])
async def login():
    data = await request.get_json()

    user_data = f"{data['user_id']}"
    app.logger.debug(user_data)
    entered_id = data['user_id']

    query = "SELECT * FROM users WHERE user_id = :id"
    row = await db.fetch_one(query=query, values={"id": entered_id})
    if row is not None:
        return jsonify({"Data found for searched ID": entered_id})
    else:
        return jsonify({"Error Message": "404 Not Found"})


@app.route("/DB")
async def db_connect():

    connection = await db.connect()
    print("connection: " + str(connection))
    return str(connection)

app.run()

