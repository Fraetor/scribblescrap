#! /usr/bin/env python3

"""Scribble Scrap."""

import flask
import sqlite3

import stuff

db = sqlite3.connect("db.sqlite3")
db.execute("CREATE TABLE IF NOT EXISTS users(user_id INT, name TEXT)")
db.execute(
    "CREATE TABLE IF NOT EXISTS scribbles(user_id INT, name TEXT, image BLOB, attack INT, defence INT, speed INT, health INT, type TEXT, type2 TEXT)"
)
del db

app = flask.Flask(__name__)
app.secret_key = b"*s\xd3\xea%\xc7\x99\x8e\xb1\x13V\rpG\xf3\x8c\xf6\xcb'J7f\xc3\xe1\xb7\r\xe2\xbe8\x1cH\xe8"


@app.get("/")
def index():
    if "username" in flask.session:
        return f'Logged in as {flask.session["username"]}'
    return "You are not logged in"


@app.post("/api/login")
def login():
    db = sqlite3.connect("db.sqlite3")
    username = flask.request.json["username"]
    print(username)
    user_id = stuff.get_user_id_from_username(db, username)
    if not user_id:
        user_id = stuff.create_user(db, username)
    flask.session["user_id"] = user_id
    resp = flask.make_response()
    resp.set_cookie("username", flask.request.json["username"])
    return resp


@app.post("/api/logout")
def logout():
    # Remove the username from the session if it's there
    resp = flask.make_response(flask.redirect(flask.url_for("index")))
    resp.set_cookie("username", expires=0)
    flask.session.pop("username", None)
    return resp


@app.post("/api/create_scribble")
def create_scribble():
    if "username" not in flask.session:
        flask.abort(401)
    return "Cool!"


if __name__ == "__main__":
    app.run(debug=True)
