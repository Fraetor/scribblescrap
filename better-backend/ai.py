from openai import OpenAI
import base64
import json

system = """
I'm going to provide you with an object, and your task is to assess
its relevance to a set of predefined categories. Determine what the
object is and write a short description of it for yourself. For each category listed
below, assign a numerical value from 0 to 100 based on how well the
object fits into that category. Please be as precise and accurate
as possible; avoid rounding to the nearest multiple of 5. Utilize
the entire numerical range from 0 to 100.

For your descriptions, you should be as definite as possible. Make
assumptions if needed. For example, don't say things like "this is
most likely an orange". Claim that it is one.

It's unlikely that the correct number for a category is zero, since
most things at least fit by some degree.

For the "nickname" field, come up with a cutesy nickname for the species
of monster. This could maybe be based on varieties of the object, parts
of the object, human names which are related, or properties of the object.
These shouldn't just be combinations of words, but more like new words
constructed from them.

We also want, at the end of the JSON object, the top ranked category.
This should go in the "Top" field. Then, if there is a second category
which comes in close, put that in the "next" field. The "next" field
should only be used if we're very sure about it, so maybe if the number
for that category is at least, say, 75. The top category should be close
to 90 or 100 in most cases, but don't force it.

Finally, there are four "stat" categories: "might", "speed", "health",
and "defence". We roll for the actual values separately, but I want
you to order the stats from highest to lowest. For example, a tank
might have high defence, then might, but low speed.

Categories and descriptions:

    humanoid: Objects resembling or possessing human-like characteristics.
        Examples: A person, a humanoid robot.

    arcane: Objects associated with mysterious or esoteric knowledge.
        Examples: A spellbook, an ancient artifact.

    bird: Objects characterized by wings or association with avian traits.
        Examples: A robin, a phoenix.

    tech: Objects that perform mechanical functions.
        Examples: A computer, a drone.

    mud: Objects consisting of soft or wet dirt or muddy water.
        Examples: A mud puddle, wet clay.

    titan: Objects of immense size or godlike stature.
        Examples: A skyscraper, a titan in mythology.

    beast: Objects representing non-humanoid, non-bird animals.
        Examples: A lion, a dragon.

    light: Objects associated with bright illumination or transparency.
        Examples: A lamp, a crystal.

    dark: Objects associated with darkness or light obstruction.
        Examples: A shadow, a black hole.

    fire: Objects capable of combustion or explosive reactions.
        Examples: A candle, a flamethrower.

    plant: Objects derived from or resembling flora or complex fungi.
        Examples: A flower, a fern.

    rock: Objects composed of hard minerals or associated with rock music.
        Examples: A boulder, a geode.

    lightning: Objects capable of generating electrical discharges or associated with lightning phenomena.
        Examples: A lightning bolt, a Tesla coil.

    gas: Objects consisting of or emitting gaseous substances.
        Examples: A cloud, a canister of helium.

    aqua: Objects composed of water or associated with underwater environments.
        Examples: A fish, a submarine.

    unreal: Objects originating from fiction or fantasy, existing beyond reality.
        Examples: A unicorn, a warp drive.

    paper: Objects composed of cellulose material, particularly white, flat sheets.
        Examples: A notebook, a newspaper.

    symbol: Abstract representations or signs.
        Examples: The yin and yang symbol, a peace sign.

    scissors: Objects characterized by sharp, metallic cutting edges.
        Examples: A pair of shears, a pocket knife.

    food: Objects intended for consumption in their current form.
        Examples: A sandwich, an apple.

    plastic: Objects made from synthetic materials, often derived from petrochemicals.
        Examples: A plastic bottle, a credit card.

    tiny: Objects that are very small, or explicitly and definitionally youthful.
        Examples: A puppy, a ladybug, a paper-clip.

    sonic: Objects related to sound emission, composition, or speed.
        Examples: A speaker, a supersonic aircraft.

    poison: Objects containing substances capable of causing harm or death.
        Examples: A venomous snake, a toxic chemical.

    spooky: Objects associated with fear, the supernatural, or death.
        Examples: A haunted house, a ghost costume.

    fabric: Objects composed of various textiles.
        Examples: A blanket, a dress.

    trash: Objects deemed useless or discarded items.
        Examples: A broken appliance, a crumpled paper.

Respond with a JSON object structured as follows:

json

{
    "object": "Coffee Cup",
    "nickname": "...",
    "description": "A plastic coffee cup with steam coming out the top.",
    "top": "titan",
    "next": null | "plastic" etc,
    "stat_ranking": [ "health", "speed", "might", "defence" ]
}

Just generate the JSON, don't output anything else, and don't put it
in backtick code fences. Don't use any comments. Just output JSON.

Also, don't output the individual numbers for each category - just output
the schema i've given.
"""

test_image = "https://i.ibb.co/yqYY7TD/4d90b291-444a-460f-a160-dd4da33688bb.png"

client = OpenAI()

def do_ai_stuff(image_path):
    b64img = encode_image(image_path)
    image_url = f"data:image/png;base64,{b64img}"

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "system",
                "content": system,
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        },
                    },
                ],
            }
        ],
        max_tokens=1500,
    )

    json_content = response.choices[0].message.content
    print(json_content)

    return json.loads(str(json_content))

def encode_image(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
