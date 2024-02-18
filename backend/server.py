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
import sys

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
    resp = flask.make_response(flask.redirect(flask.url_for("index")))
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
    scribble_id = str(uuid4())

    # Process image.
    image_path = tempfile.mktemp(".jpg")
    next(flask.request.files.values()).save(image_path)
    db.set(f"{user_id}:raw_mon", image_path)
    print("Temp image saved to", image_path)
    # Request to cropping server.
    response = requests.get(
        IMAGE_CROPPER_URL + f"/segment?path={urllib.parse.quote_plus(image_path)}"
    )
    if not response.ok:
        print(response.text)
        flask.abort(502)
    processing_id = response.text
    response = requests.get(IMAGE_CROPPER_URL + f"/get/{processing_id}")
    if not response.ok:
        print(response.text)
        flask.abort(502)
    image = response.content
    db.lpush(f"{user_id}:scribbles", scribble_id)
    db.set(f"{user_id}:{scribble_id}:image", image)
    # Keep hold of processing_id for generating the stats.
    db.set(f"{user_id}:{scribble_id}:processing_id", processing_id)
    os.unlink(image_path)

    return scribble_id


@app.get("/api/scribbles")
def list_scribbles():
    if "user_id" not in flask.session:
        flask.abort(401)
    user_id = flask.session["user_id"]
    scribble_ids = [
        id.decode("UTF-8") for id in db.lrange(f"{user_id}:scribbles", 0, -1)
    ]
    print(scribble_ids)
    return scribble_ids


@app.get("/api/scribble/<scribble_id>/image")
def scribble_image(scribble_id):
    if "user_id" not in flask.session:
        flask.abort(401)
    user_id = flask.session["user_id"]
    image = db.get(f"{user_id}:{scribble_id}:image")
    resp = flask.make_response(image)
    resp.headers["Content-type"] = "image/png"
    return resp


@app.get("/api/scribble/<scribble_id>/limbs")
def scribble_limbs(scribble_id):
    return get_limbs(scribble_id)


def get_limbs(scribble_id):
    if "user_id" not in flask.session:
        flask.abort(401)
    user_id = flask.session["user_id"]
    raw_limbs = db.get(f"{user_id}:{scribble_id}:limbs")
    if raw_limbs is None:
        processing_id = db.get(f"{user_id}:{scribble_id}:processing_id").decode("utf-8")
        print("Getting:", IMAGE_CROPPER_URL + f"/limbs/{processing_id}")
        response = requests.get(IMAGE_CROPPER_URL + f"/limbs/{processing_id}")
        if not response.ok:
            print(response.text)
            flask.abort(502)
        limbs = response.json()
        print("new limbs=", limbs)
        db.set(f"{user_id}:{scribble_id}:limbs", json.dumps(limbs))
    else:
        limbs = json.loads(raw_limbs)
    return limbs


@app.post("/api/scribble/<scribble_id>/generate")
def scribble_generate(scribble_id):
    if "user_id" not in flask.session:
        flask.abort(401)
    user_id = flask.session["user_id"]

    raw_scribble_info = db.get(f"{user_id}:{scribble_id}:info")
    if raw_scribble_info is None:
        # Generate scribble info.
        processing_id = db.get(f"{user_id}:{scribble_id}:processing_id").decode("utf-8")
        print("Getting:", IMAGE_CROPPER_URL + f"/calculate-stats/{processing_id}")
        response = requests.get(IMAGE_CROPPER_URL + f"/calculate-stats/{processing_id}")
        if not response.ok:
            print(response.text)
            flask.abort(502)
        scribble_info = response.json()
        scribble_info["image"] = f"/api/scribble/{scribble_id}/image"
        scribble_info["arm_image"] = "/public/arm.png"
        scribble_info["eye_image"] = "/public/eye.png"
        scribble_info["leg_image"] = "/public/leg.png"
        db.set(f"{user_id}:{scribble_id}:info", json.dumps(scribble_info))
    else:
        scribble_info = json.load(raw_scribble_info)
    return scribble_info


@app.get("/api/scribble/<scribble_id>/info")
def scribble_info(scribble_id):
    if "user_id" not in flask.session:
        flask.abort(401)
    user_id = flask.session["user_id"]
    raw_scribble_info = db.get(f"{user_id}:{scribble_id}:info")
    if raw_scribble_info is None:
        limbs = get_limbs(scribble_id)
        print(limbs)
        scibble_info = {
            "image": f"/api/scribble/{scribble_id}/image",
            "arm_image": "/public/arm.png",
            "eye_image": "/public/eye.png",
            "leg_image": "/public/leg.png",
            "arms": limbs["arms"],
            "legs": limbs["legs"],
        }
    else:
        scibble_info = json.loads(raw_scribble_info)
    return scibble_info


if __name__ == "__main__":
    app.run(debug=True)
