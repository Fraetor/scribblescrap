#! /usr/bin/env python3

"""Scribble Scrap."""

import json
import os
import sys
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
    resp.set_cookie("username", flask.request.json["username"], path="/")
    return resp


@app.route("/api/logout")
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
    processing_id = requests.get(
        IMAGE_CROPPER_URL + f"/segment?path={urllib.parse.quote_plus(image_path)}"
    ).text
    response = requests.get(IMAGE_CROPPER_URL + f"/get/{processing_id}")
    image = response.content
    scribble_id = str(uuid4())
    db.rpush(f"{user_id}:scribbles", scribble_id)
    db.set(f"{user_id}:{scribble_id}:image", image)
    os.unlink(image_path)

    # Get scribble's stats
    print(
        "Getting:",
        IMAGE_CROPPER_URL + f"/calculate-stats/{processing_id}",
        file=sys.stderr,
    )
    response = requests.get(IMAGE_CROPPER_URL + f"/calculate-stats/{processing_id}")
    # print(response.text, file=sys.stderr)
    scribble_info = response.json()
    scribble_info["image"] = f"/api/scribble/{scribble_id}/image"
    scribble_info["arm_image"] = "/public/arm.png"
    scribble_info["eye_image"] = "/public/eye.png"
    scribble_info["leg_image"] = "/public/leg.png"
    db.set(f"{user_id}:{scribble_id}:info", json.dumps(scribble_info))
    return scribble_id


@app.get("/api/scribbles")
def list_scribbles():
    if "user_id" not in flask.session:
        flask.abort(401)
    user_id = flask.session["user_id"]
    scribble_ids = db.lrange(f"{user_id}:scribbles", 0, -1)
    print(scribble_ids)
    resp = flask.jsonify(scribble_ids)
    return resp


@app.get("/api/scribble/<scribble_id>/image")
def scribble_image(scribble_id):
    if "user_id" not in flask.session:
        flask.abort(401)
    user_id = flask.session["user_id"]
    image = db.get(f"{user_id}:{scribble_id}:image")
    resp = flask.make_response(image)
    resp.headers["Content-Type"] = "image/png"
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
