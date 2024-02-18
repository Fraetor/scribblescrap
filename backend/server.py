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


def make_qr_code(text: str) -> bytes:
    response = requests.get(
        f"https://qrcode.show/{urllib.parse.quote(text)}",
        headers={"Accept": "image/png"},
    )
    if not response.ok:
        raise OSError("QR generation failed.")
    return response.content


@app.route("/api/new_battle")
def create_new_battle():
    if "user_id" not in flask.session:
        flask.abort(401)
    battle_id = str(uuid4())
    db.set(
        f"{battle_id}:qr",
        make_qr_code(f"https://scribble-scraps.frost.cx/api/{battle_id}/join"))
    return battle_id


@app.get("/api/<battle_id>/qr")
def battle_qr(battle_id):
    qr_png = db.get(f"{battle_id}:qr")
    return qr_png


@app.route("/api/<battle_id>/join/<scribble_id>")
def join_battle(battle_id, scribble_id):
    if "user_id" not in flask.session:
        flask.abort(401)
    user_id = flask.session["user_id"]
    db.lpush(f"{battle_id}:users", user_id)
    db.set(f"{battle_id}:{user_id}:scribble", scribble_id)
    return user_id

@app.route("/api/<battle_id>/join")
def join_battle_no_scribble(battle_id):
    if "user_id" not in flask.session:
        flask.abort(401)
    user_id = flask.session["user_id"]
    db.lpush(f"{battle_id}:users", user_id)

    scribble_ids = [
        id.decode("UTF-8") for id in db.lrange(f"{user_id}:scribbles", 0, -1)
    ]

    db.set(f"{battle_id}:{user_id}:scribble", scribble_ids[0])

    return flask.redirect("/battle?id=" + battle_id)

@app.get("/api/<battle_id>/status")
def battle_status(battle_id):
    players = db.lrange(f"{battle_id}:users", 0, -1)
    user_id_1 = players[0].decode("UTF-8")
    if len(players) == 2:
        user_id_2 = players[1].decode("UTF-8")
        user_2 = {
            "user_id": user_id_2,
            "scribble_id": db.get(f"{battle_id}:{user_id_2}:scribble").decode("utf-8"),
        }
    else:
        user_2 = None

    battle_status = {
        "battle_id": battle_id,
        "player1": {
            "user_id": user_id_1,
            "scribble_id": db.get(f"{battle_id}:{user_id_1}:scribble").decode("utf-8"),
        },
        "player2": user_2,
    }
    return battle_status


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
    db.set(f"{scribble_id}:image", image)
    # Keep hold of processing_id for generating the stats.
    db.set(f"{scribble_id}:processing_id", processing_id)
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
    image = db.get(f"{scribble_id}:image")
    resp = flask.make_response(image)
    resp.headers["Content-type"] = "image/png"
    return resp


@app.get("/api/scribble/<scribble_id>/limbs")
def scribble_limbs(scribble_id):
    return get_limbs(scribble_id)


def get_limbs(scribble_id):
    raw_limbs = db.get(f"{scribble_id}:limbs")
    if raw_limbs is None:
        processing_id = db.get(f"{scribble_id}:processing_id").decode("utf-8")
        print("Getting:", IMAGE_CROPPER_URL + f"/limbs/{processing_id}")
        response = requests.get(IMAGE_CROPPER_URL + f"/limbs/{processing_id}")
        if not response.ok:
            print(response.text)
            flask.abort(502)
        limbs = response.json()
        print("new limbs=", limbs)
        db.set(f"{scribble_id}:limbs", json.dumps(limbs))
    else:
        limbs = json.loads(raw_limbs)
    return limbs


@app.post("/api/scribble/<scribble_id>/generate")
def scribble_generate(scribble_id):
    if "user_id" not in flask.session:
        flask.abort(401)
    raw_scribble_info = db.get(f"{scribble_id}:info")
    if raw_scribble_info is None:
        # Generate scribble info.
        processing_id = db.get(f"{scribble_id}:processing_id").decode("utf-8")
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
        db.set(f"{scribble_id}:info", json.dumps(scribble_info))
    else:
        scribble_info = json.load(raw_scribble_info)
    return scribble_info


@app.get("/api/scribble/<scribble_id>/info")
def scribble_info(scribble_id):
    raw_scribble_info = db.get(f"{scribble_id}:info")
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
