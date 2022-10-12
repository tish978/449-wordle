from quart import Quart, request, jsonify
from quart_schema import QuartSchema #, DataSource, validate_request
import sqlalchemy
from sqlalchemy import create_engine, insert, select, Table, Column, Integer, String
from databases import Database
import socket
from dataclasses import dataclass
from flask import render_template, abort


engine = create_engine('sqlite:///C:/Users/bruht/PycharmProjects/quart-test/testDB.db', echo=False)
db = Database('sqlite:///C:/Users/bruht/PycharmProjects/quart-test/testDB.db')
#engine = create_engine('sqlite:///home/students/Documents')


##EXAMPLE DB/SQL-ALCHEMY CODE
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("password", String(length=100))
)

metadata.create_all(engine)

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

    stmt = (
        insert(users).
        values(user_id=entered_id, password=entered_pass)
    )
    engine.execute(stmt)

    return jsonify({"Account created with ID": entered_id})


@app.route("/login", methods=["POST"])
async def login():
    data = await request.get_json()

    user_data = f"{data['user_id']}"
    app.logger.debug(user_data)
    entered_id = data['user_id']

    query = select(users).where(users.c.user_id == entered_id)
    if engine.connect().execute(query) is not None:
        print("NONE")

    if select(users).where(users.c.user_id == entered_id) is not None:
        stmt = select(users).where(users.c.user_id == entered_id)
        with engine.connect() as conn:
            if conn.execute(stmt).fetchone() is None:
                return "404 Not Found"
            try:
                for row in conn.execute(stmt).fetchall():
                    return jsonify({"Data found for searched ID": entered_id})
            except:
                print("An exception occurred")
    else:
        return jsonify({"Data NOT FOUND for searched ID": entered_id})



@app.route("/DB")
async def db_connect():

    connection = engine.connect()
    print("connection: " + str(connection))
    return str(connection)

app.run()

