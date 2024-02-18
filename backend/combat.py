# Online Python - IDE, Editor, Compiler, Interpreter

Damage = Hitrate = Moveblock = Dodge = DamageReduction = Resistance = Health = Maxhealth = {"Value":55, "EffectiveValue":55, "PositiveMultiplier":1, "PositiveMultiplierTimer":0, "PositiveIncrement":0, "NegativeMultiplier":1, "NegativeMultiplierTimer":0, "NegativeIncrement":0}

Statlist =["Damage", "Hitrate", "MoveBlock", "Dodge", "DamageReduction", "Resistance", "Health","MaxHealth", "Charge"]

bleed = ["Poison",0]

scrapling_state = {
"Damage":Damage,
"Hitrate": Hitrate,
"Moveblock": Moveblock,
"Dodge": Dodge,
"DamageReduction": DamageReduction,
"Resistance": Resistance,
"Health": Health,
"MaxHealth": MaxHealth,
"Charge": False,
"Bleed": bleed
}

scrapling_ids = ["asdf", "gfbg", "ifdjsg", "gfyh", "gfdfg", "fgfg4"]

p1_state = {
    "Scraplings" = {},
    "id" = "werwerwer",
    "Turn" = True}

for a in scrapling_ids:
    p1_state["Scraplings"][a] = scrapling_state

p1_state = p2_state

turnblock = 0

active_scraplings =  ["asdf", "gfbg"]

state = [p1_state:dict, p2_state:dict, turn_block, active_scraplings]

def Update_Battle(state:list, current_action:dict):
    playerstate = state[:2]
    for player in playerstate:
        for scrapling_key in player["Scraplings"]:
            scrapling = player[scrapling_key]
            for state_key in scrapling:
                if (state_key != "Charge") and (state_key != "Bleed"):
                    state = scrapling[state_key]
                    for stat_key in state:
                        stat = state[stat_key]
                        if stat["PositiveMultiplierTimer"] > 0:
                            stat["PositiveMultiplierTimer"] -= 1
                        if stat["NegativeMultiplierTimer"] > 0:
                            stat["NegativeMultiplierTimer"] -= 1
                        if stat["PositiveMultiplierTimer"] <= 0:
                            stat["PositiveMultiplierTimer"] = 0
                            stat["PositiveMultiplier"] = 1
                        if stat["NegativeMultiplierTimer"] <= 0:
                            stat["NegativeMultiplierTimer"] = 0
                            stat["NegativeMultiplier"] = 1
                        stat["EffectiveValue"] = stat["Value"]*stat["PositiveMultiplier"]*stat["NegativeMultiplier"]+stat["PositiveIncrement"]+stat["NegativeIncrement"]
                        if stat_key == "Damage" and state["Charge"] == True:
                            stat["EffectiveValue"] = 3*stat["EffectiveValue"]
                elif state key == "Bleed"
                    bleed_damage = scrapling[state_key][1]
                    state["Health"]["Value"] = state["Health"]["Value"] - bleed_damage
                    if scrapling[state_key][1] > 0:
                        scrapling[state_key][1] = scrapling[state_key][1] -1
                    else:
                        scrapling[state_key][1] = 0
    state[0] = playerstate[0]
    state[1] = playerstate[1]
    if turnblock >= 0:
        player_turn = 0
    else:
        player_turn = 1
    if state[3]
    if current_action[:6] == "Switch":
        print("Sad")
    elif current_action == "Charge":
        state[player_turn][active_scraplings[player_turn]][]
        