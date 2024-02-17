#! /usr/bin/env python3

"""Scribble Scrap."""

import json
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
    next(flask.request.files.values()).save(image_path)
    db.set(f"{user_id}:raw_mon", image_path)
    print("Temp image saved to", image_path)
    # Request to cropping server.
    # TODO: Enable the actual server.
    with open(image_path, "rb") as fp:
        image = fp.read()
    # processing_id = requests.get(
    #     IMAGE_CROPPER_URL + f"?path={urllib.parse.quote_plus(image_path)}"
    # )
    # response = requests.get(IMAGE_CROPPER_URL + f"/get/{processing_id.text}")
    # image = response.content
    scribble_id = str(uuid4())
    db.set(f"{user_id}:{scribble_id}:image", image)
    os.unlink(image_path)

    # Get scribble's stats
    # TODO: AI calls.

    # TODO: This needs the AI returns put into it.
    scribble_info = {
        "image": flask.url_for(f"/api/scribble/{scribble_id}/image"),
        "arm_image": "/public/arm.png",
        "eye_image": "/public/eye.png",
        "leg_image": "/public/leg.png",
        "health": {"max": 25},
        "limbs": [
            {"direction": "2", "arm_anchor": [10, 15], "body_anchor": [25, 20]},
            {"direction": "4.3", "arm_anchor": [10, 15], "body_anchor": [25, 20]},
        ],
        "name": "Testimon",
        "description": "A test scraplet.",
        "stats": {"might": 1, "speed": 1, "health": 1, "defence": 1},
        "types": [
            {"name": "grass", "colour": "#00ff00"},
            {"name": "brick", "colour": "#ff0c00"},
        ],
    }
    db.set(f"{user_id}:{scribble_id}:info", json.dumps(scribble_info))
    return scribble_info


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
    image = db.get(f"{user_id}:{scribble_id}:image")
    return image


@app.get("/api/scribble/<scribble_id>/info")
def scribble_info(scribble_id):
    if "user_id" not in flask.session:
        flask.abort(401)
    user_id = flask.session["user_id"]
    scribble_info = json.loads(db.get(f"{user_id}:{scribble_id}:info"))
    return scribble_info


if __name__ == "__main__":
    app.run(debug=True)
