# Online Python - IDE, Editor, Compiler, Interpreter

import random
import math

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
    "Scraplings" : {},
    "id" : "werwerwer",
    "Turn" : True
    }

for a in scrapling_ids:
    p1_state["Scraplings"][a] = scrapling_state

p1_state = p2_state

turnblock = 0

active_scraplings =  ["asdf", "gfbg"]

state = [p1_state, p2_state, turn_block, active_scraplings]

def modify_stat(stat_name, scrapling):
    pass


def update_modifiers(state:list):
    playerstate = state[:2]
    for player in playerstate:
        for scrapling_key in player["Scraplings"]:
            scrapling = player[scrapling_key]
            for state_key in scrapling:
                if (state_key != "Charge") and (state_key != "Bleed"):
                    stats = scrapling[state_key]
                    for stat_key in stats:
                        stat = stats[stat_key]
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
                elif state_key == "Bleed":
                    bleed_damage = scrapling[state_key][1]
                    state["Health"]["Value"] = state["Health"]["Value"] - bleed_damage
                    if scrapling[state_key][1] > 0:
                        scrapling[state_key][1] = scrapling[state_key][1] -1
                    else:
                        scrapling[state_key][1] = 0
    state[0] = playerstate[0]
    state[1] = playerstate[1]
    return state

speed = {
    "VerySlow" : 4,
    "Slow" : 2,
    "Normal" : 1,
    "Fast" : 0.5,
    "VeryFast": 0.25,
    "Instant": 0
}

accuracy = {
    "VeryInaccurate" : -1,
    "Inaccurate" : -0.5,
    "Normal" : 1,
    "Accurate" : 2,
    "Very Accurate" : 4,
    "Guaranteed" : 999
}

damage = {
    "VeryWeak" : 0.25,
    "Weak" : 0.5,
    "Normal" : 1,
    "High" : 2,
    "VeryHigh": 4,
    "Lethal": 999
}

armour_piercing = {
    "None" : 0,
    "Low" : 30,
    "High" : 60,
    "Full" : 999
}

def update_action(state:list, current_action:dict):
    state = update_modifiers(state)

    if player_turn == 0:
        speedsign = -1
    else:
        speedsign = 1

    if turnblock >= 0:
        player_turn = 0
    else:
        player_turn = 1
    action_result = ["","", ""]
    if current_action["Type"] == "Switch":
        state[3][player_turn] = current_action["ID"]
        state[2] = state[2] + speedsign * state[player_turn]["Scraplings"][active_scraplings[player_turn]]["MoveBlock"]["EffectiveValue"]

        if (player_turn == 0) and state[2] >= 0:
            state[2] = -1
        elif (player_turn == 1) and state[2] < 0:
            state[2] = 0
        
    elif current_action == "Charge":
        state[player_turn]["Scraplings"][active_scraplings[player_turn]]["Charge"] = True
        time = state[player_turn]["Scraplings"][active_scraplings[player_turn]]["MoveBlock"]["EffectiveValue"]
    
    elif current_action == "Chip":
        action_result = attack(state[player_turn]["Scraplings"][active_scraplings[player_turn]], state[1-player_turn]["Scraplings"][active_scraplings[1-player_turn]], speed["Normal"], accuracy["Normal"], damage["Normal"], armour_piercing["None"],1)
        state[player_turn]["Scraplings"][active_scraplings[player_turn]]["DamageReduction "]["NegativeIncrement"]-=5
    elif current_action == "Leech":
        action_result = attack(state[player_turn]["Scraplings"][active_scraplings[player_turn]], state[1-player_turn]["Scraplings"][active_scraplings[1-player_turn]], speed["Normal"], accuracy["Normal"], damage["Normal"], armour_piercing["None"],1)
        state[player_turn]["Scraplings"][active_scraplings[player_turn]]["Health "]["Value"]+=math.trunc(action_result[1]/2)
    elif current_action == "Serenity":
        action_result = [0, 0, state[player_turn]["Scraplings"][active_scraplings[player_turn]]["Moveblock"]["EffectiveValue"]]
        state[player_turn]["Scraplings"][active_scraplings[player_turn]]["Health "]["Value"]+=10
        state[player_turn]["Scraplings"][active_scraplings[player_turn]]["Damage"]["NegativeMultiplier"]=1
        state[player_turn]["Scraplings"][active_scraplings[player_turn]]["Damage "]["NegativeMultiplier"]=1
        state[player_turn]["Scraplings"][active_scraplings[player_turn]]["Damage "]["NegativeMultiplier"]=1
        state[player_turn]["Scraplings"][active_scraplings[player_turn]]["Damage "]["NegativeMultiplier"]=1
        state[player_turn]["Scraplings"][active_scraplings[player_turn]]["Damage "]["NegativeMultiplier"]=1
        state[player_turn]["Scraplings"][active_scraplings[player_turn]]["Damage "]["NegativeMultiplier"]=1
        state[player_turn]["Scraplings"][active_scraplings[player_turn]]["Damage "]["NegativeMultiplier"]=1
        state[player_turn]["Scraplings"][active_scraplings[player_turn]]["Damage "]["NegativeMultiplier"]=1
        state[player_turn]["Scraplings"][active_scraplings[player_turn]]["Damage "]["NegativeMultiplier"]=1
        state[player_turn]["Scraplings"][active_scraplings[player_turn]]["Damage "]["NegativeMultiplier"]=1
        state[player_turn]["Scraplings"][active_scraplings[player_turn]]["Damage "]["NegativeMultiplier"]=1
        state[player_turn]["Scraplings"][active_scraplings[player_turn]]["Damage "]["NegativeMultiplier"]=1
        state[player_turn]["Scraplings"][active_scraplings[player_turn]]["Damage "]["NegativeMultiplier"]=1
        state[player_turn]["Scraplings"][active_scraplings[player_turn]]["Damage "]["NegativeMultiplier"]=1
        state[player_turn]["Scraplings"][active_scraplings[player_turn]]["Damage "]["NegativeMultiplier"]=1

    elif current_action == "Softening Strike":
        action_result = attack(state[player_turn]["Scraplings"][active_scraplings[player_turn]], state[1-player_turn]["Scraplings"][active_scraplings[1-player_turn]], speed["Normal"], accuracy["Normal"], damage["Normal"], armour_piercing["None"],1)
    elif current_action == "Barrage":
        action_result = attack(state[player_turn]["Scraplings"][active_scraplings[player_turn]], state[1-player_turn]["Scraplings"][active_scraplings[1-player_turn]], speed["Normal"], accuracy["Normal"], damage["Normal"], armour_piercing["None"],1)
    elif current_action == "Detonation":
        action_result = attack(state[player_turn]["Scraplings"][active_scraplings[player_turn]], state[1-player_turn]["Scraplings"][active_scraplings[1-player_turn]], speed["Normal"], accuracy["Normal"], damage["Normal"], armour_piercing["None"],1)
    elif current_action == "Evasive Strike":
        action_result = attack(state[player_turn]["Scraplings"][active_scraplings[player_turn]], state[1-player_turn]["Scraplings"][active_scraplings[1-player_turn]], speed["Normal"], accuracy["Normal"], damage["Normal"], armour_piercing["None"],1)
    elif current_action == "Sticky Strike":
        action_result = attack(state[player_turn]["Scraplings"][active_scraplings[player_turn]], state[1-player_turn]["Scraplings"][active_scraplings[1-player_turn]], speed["Normal"], accuracy["Normal"], damage["Normal"], armour_piercing["None"],1)
    elif current_action == "Drain Attack":
        action_result = attack(state[player_turn]["Scraplings"][active_scraplings[player_turn]], state[1-player_turn]["Scraplings"][active_scraplings[1-player_turn]], speed["Normal"], accuracy["Normal"], damage["Normal"], armour_piercing["None"],1)
    elif current_action == "Quick Attack":
        action_result = attack(state[player_turn]["Scraplings"][active_scraplings[player_turn]], state[1-player_turn]["Scraplings"][active_scraplings[1-player_turn]], speed["Normal"], accuracy["Normal"], damage["Normal"], armour_piercing["None"],1)
    elif current_action == "Magic Missile":
        action_result = attack(state[player_turn]["Scraplings"][active_scraplings[player_turn]], state[1-player_turn]["Scraplings"][active_scraplings[1-player_turn]], speed["Normal"], accuracy["Normal"], damage["Normal"], armour_piercing["None"],1)
    elif current_action == "Ghost Dart":
        action_result = attack(state[player_turn]["Scraplings"][active_scraplings[player_turn]], state[1-player_turn]["Scraplings"][active_scraplings[1-player_turn]], speed["Normal"], accuracy["Normal"], damage["Normal"], armour_piercing["None"],1)
    elif current_action == "Dispelling Strike":
        action_result = attack(state[player_turn]["Scraplings"][active_scraplings[player_turn]], state[1-player_turn]["Scraplings"][active_scraplings[1-player_turn]], speed["Normal"], accuracy["Normal"], damage["Normal"], armour_piercing["None"],1)
    elif current_action == "Paralysing Strike":
        action_result = attack(state[player_turn]["Scraplings"][active_scraplings[player_turn]], state[1-player_turn]["Scraplings"][active_scraplings[1-player_turn]], speed["Normal"], accuracy["Normal"], damage["Normal"], armour_piercing["None"],1)
    elif current_action == "Fortified Strike":
        action_result = attack(state[player_turn]["Scraplings"][active_scraplings[player_turn]], state[1-player_turn]["Scraplings"][active_scraplings[1-player_turn]], speed["Normal"], accuracy["Normal"], damage["Normal"], armour_piercing["None"],1)
    elif current_action == "Full Heal":
        action_result = attack(state[player_turn]["Scraplings"][active_scraplings[player_turn]], state[1-player_turn]["Scraplings"][active_scraplings[1-player_turn]], speed["Normal"], accuracy["Normal"], damage["Normal"], armour_piercing["None"],1)
    elif current_action == "Inaccurate Devastator":
        action_result = attack(state[player_turn]["Scraplings"][active_scraplings[player_turn]], state[1-player_turn]["Scraplings"][active_scraplings[1-player_turn]], speed["Normal"], accuracy["Normal"], damage["Normal"], armour_piercing["None"],1)
    elif current_action == "Grazing Attack":
        action_result = attack(state[player_turn]["Scraplings"][active_scraplings[player_turn]], state[1-player_turn]["Scraplings"][active_scraplings[1-player_turn]], speed["Normal"], accuracy["Normal"], damage["Normal"], armour_piercing["None"],1)
    elif current_action == "Bleed Attack":
        action_result = attack(state[player_turn]["Scraplings"][active_scraplings[player_turn]], state[1-player_turn]["Scraplings"][active_scraplings[1-player_turn]], speed["Normal"], accuracy["Normal"], damage["Normal"], armour_piercing["None"],1)
    
    if action_result != ["","",""]:
        time = action_result[2]

    state[2] = state[2] + speedsign * time







def attack(attacker, defender, speed, accuracy, damage, armour_piercing, attack_number):
    successes = 0
    damage = 0
    for i in range(attack_number):
        if 2*(random.randint(1,100)+random.randint(1,100))+attacker["Hitrate"]["EffectiveValue"]-defender["Dodge"]["EffectiveValue"]+accuracy*30 >= 140:
            successes +=1
    for i in range(successes):
        totaldamage = random.randint(1,attacker["Damage"]["EffectiveValue"])*damage+random.randint(1,attacker["Damage"]["EffectiveValue"])*damage - max(0,(random.randint(1,defender["DamageReduction"]["EffectiveValue"])-armour_piercing))
    attacker["Health"]["Value"] = max(0, attacker["Health"]["Value"]-totaldamage)
    time = attacker["Moveblock"]["EffectiveValue"]*speed
    return[successes, totaldamage, time]


