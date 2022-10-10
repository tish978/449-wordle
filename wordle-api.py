from quart import Quart
from quart_schema import QuartSchema
import sqlalchemy
from sqlalchemy import create_engine
from databases import Database
import socket


##EXAMPLE DB/SQL-ALCHEMY CODE
metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("password", sqlalchemy.String(length=100))
)


engine = create_engine('sqlite:///home/students/Documents')

app = Quart(__name__)
QuartSchema(app)

@app.route("/")
async def index():
    return "hello"

@app.route("/DB")
async def db_connect():

    connection = engine.connect()
    print("connection: " + str(connection))
    return str(connection)

app.run()

