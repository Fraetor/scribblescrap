#! /usr/bin/env python3

"""Scribble Scrap."""

import flask

app = flask.Flask(__name__)
app.secret_key = b"*s\xd3\xea%\xc7\x99\x8e\xb1\x13V\rpG\xf3\x8c\xf6\xcb'J7f\xc3\xe1\xb7\r\xe2\xbe8\x1cH\xe8"


@app.get("/")
def index():
    if "username" in flask.session:
        return f'Logged in as {flask.session["username"]}'
    return "You are not logged in"


@app.post("/api/login")
def login():
    flask.session["username"] = flask.request.json["username"]
    return flask.redirect(flask.url_for("index"))


@app.post("/api/logout")
def logout():
    # Remove the username from the session if it's there
    flask.session.pop("username", None)
    return flask.redirect(flask.url_for("index"))


@app.post("/api/create_scribble")
def create_scribble():
    if "username" not in flask.session:
        flask.abort(401)
    return "Cool!"


if __name__ == "__main__":
    app.run(debug=True)
