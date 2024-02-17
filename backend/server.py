#! /usr/bin/env python3

"""Scribble Scrap."""

import os
import tempfile
import urllib.parse
from uuid import uuid4

import flask
import redis
import requests


# Constants:

IMAGE_CROPPER_URL = "http://localhost:7001"


db = redis.Redis()

app = flask.Flask(__name__)
app.secret_key = b"*s\xd3\xea%\xc7\x99\x8e\xb1\x13V\rpG\xf3\x8c\xf6\xcb'J7f\xc3\xe1\xb7\r\xe2\xbe8\x1cH\xe8"


@app.get("/")
def index():
    if "username" in flask.session:
        return f'Logged in as {flask.session["username"]}'
    return "You are not logged in"


@app.post("/api/login")
def login():
    username = flask.request.json["username"]
    user_id = db.get(f"user_id:{username}")
    if user_id is None:
        print("Creating account for", username)
        user_id = str(uuid4())
        db.set(f"user_id:{username}", user_id)
    print(username, "logged in.")
    flask.session["user_id"] = user_id
    resp = flask.make_response()
    resp.set_cookie("username", flask.request.json["username"])
    return resp


@app.post("/api/logout")
def logout():
    # Remove the username from the session if it's there
    resp = flask.make_response(flask.redirect(flask.url_for("index")))
    resp.set_cookie("username", expires=0)
    flask.session.pop("user_id", None)
    return resp


@app.post("/api/create_scribble")
def create_scribble():
    if "user_id" not in flask.session:
        flask.abort(401)
    user_id = flask.session["user_id"]

    # Process image.
    image_path = tempfile.mktemp(".jpg")
    flask.request.files[0].save(image_path)
    db.set(f"{user_id}:raw_mon", image_path)
    # Request to cropping server.
    processing_id = requests.get(
        IMAGE_CROPPER_URL + f"?path={urllib.parse.quote_plus(image_path)}"
    )
    response = requests.get(IMAGE_CROPPER_URL + f"/get/{processing_id.text}")
    image = response.content
    scribble_id = str(uuid4())
    db.set(f"{user_id}:{scribble_id}:image", image)
    os.unlink(image_path)

    # Get scribble's stats
    # TODO: AI calls.
    return scribble_id


@app.get("/api/scribbles")
def list_scribbles(user_id):
    if "user_id" not in flask.session:
        flask.abort(401)
    user_id = flask.session["user_id"]
    db.get(f"{user_id}:scribbles")


@app.get("/api/scribble/<scribble_id>/image")
def scribble_image(scribble_id):
    if "user_id" not in flask.session:
        flask.abort(401)
    user_id = flask.session["user_id"]
    image: bytes = db.get(f"{user_id}:{scribble_id}:image")
    return image


if __name__ == "__main__":
    app.run(debug=True)
