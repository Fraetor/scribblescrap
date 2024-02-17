#! /usr/bin/env python3

"""Doodlemon."""

from flask import Flask, session, request, redirect, url_for

app = Flask(__name__)
app.secret_key = b"*s\xd3\xea%\xc7\x99\x8e\xb1\x13V\rpG\xf3\x8c\xf6\xcb'J7f\xc3\xe1\xb7\r\xe2\xbe8\x1cH\xe8"


@app.get("/")
def index():
    if "username" in session:
        return f'Logged in as {session["username"]}'
    return "You are not logged in"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        return redirect(url_for("index"))
    return """
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    """


@app.route("/logout")
def logout():
    # remove the username from the session if it's there
    session.pop("username", None)
    return redirect(url_for("index"))
