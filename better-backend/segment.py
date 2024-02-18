from rembg import remove, new_session
from PIL import Image, ImageDraw
from flask import Flask, request, send_file
import uuid
import os

from borders import *
from ai import *
from roll import *

app = Flask(__name__)

output_dir = "images/"

session = new_session()

@app.route("/")
def index():
    return "segment api (/segment, /get)"

@app.route("/segment")
def segment_path():
    path = request.args.get("path")
    if path == None:
        return "no uri given", 400

    try:
        input = Image.open(path)
    except FileNotFoundError:
        return "file does not exist", 404

    id = str(uuid.uuid4())
    smaller = preprocess(input)
    output = remove(input, session=session)
    processed = postprocess(output)

    processed.save(os.path.join(output_dir, id + ".png"))

    return id, 200

@app.route("/get/<uuid:id>")
@app.route("/get/<uuid:id>.png")
def get_uuid(id):
    return send_file(
        os.path.join(output_dir, str(id) + ".png"),
        download_name="output.png"
    )

@app.route("/calculate-stats/<uuid:id>")
@app.route("/calculate-stats/<uuid:id>.png")
def calculate_stats(id):
    data = do_ai_stuff(os.path.join(output_dir, str(id) + ".png"))

    types = [data["top"].lower()]
    if "next" in data:
        types.append(data["next"].lower())

    stats = choose_stats(data["stat_ranking"])

    print(data)

    return {
        "name": data["object"].title(),
        "nickname": data["nickname"].title(),
        "description": data["description"],
        "types": types,
        "arms": [
            {
                "direction": -0.1,
                "limb_anchor": [10, 10],
                "body_anchor": [154, -15],
            },
            {
                "direction": 3.241,
                "limb_anchor": [10, 10],
                "body_anchor": [-154, -15],
            },
        ],
        "legs": [
            {
                "direction": 1.471,
                "limb_anchor": [10, 30],
                "body_anchor": [70, 130],
            },
            {
                "direction": 1.671,
                "limb_anchor": [10, 30],
                "body_anchor": [-70, 120],
            },
        ],
        "arm_image": "arm.png",
        "leg_image": "leg.png",
        "health": {
            "max": stats["health"] * 4,
        },
        "stats": stats
    }
