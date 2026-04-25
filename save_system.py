import game_state
import json
from pathlib import Path

def build_save_dictionary():
    save_dictionary = {"tick_rate": game_state.tick_rate,
                       "tick_count": game_state.tick_count,
                       "souls": game_state.souls,
                       "souls_multiplier": game_state.souls_multiplier,
                       "total_souls_gained": game_state.total_souls_gained,
                       "total_souls_spent": game_state.total_souls_spent,
                       "click_count": game_state.click_count,
                       "click_power": game_state.click_power,
                       "undead": {
                           "skeleton": {
                               "count": game_state.skeleton.count,
                               "cost": game_state.skeleton.cost,
                               "cost_multiplier": game_state.skeleton.cost_multiplier,
                               "power": game_state.skeleton.power
                       },
                           "zombie": {
                               "count": game_state.zombie.count,
                               "cost": game_state.zombie.cost,
                               "cost_multiplier": game_state.zombie.cost_multiplier,
                               "power": game_state.zombie.power
                       },
                            "wraith": {
                               "count": game_state.wraith.count,
                               "cost": game_state.wraith.cost,
                               "cost_multiplier": game_state.wraith.cost_multiplier,
                               "power": game_state.wraith.power
                       }
                       },
                       "upgrades_status": {
                           
                       }
                       }
    upgrades_status = save_dictionary["upgrades_status"]
    for upgrade in game_state.upgrades:
        upgrade_id = upgrade["id"]
        upgrade_bought = upgrade["bought"]
        upgrades_status[str(upgrade_id)] = upgrade_bought
    return save_dictionary

def load_save_from_dictionary(save_dictionary):
    undead = save_dictionary["undead"]
    skeleton = undead["skeleton"]
    zombie = undead["zombie"]
    wraith = undead["wraith"]
    #Loading Global Variables
    game_state.tick_rate = int(save_dictionary["tick_rate"])
    game_state.tick_count = int(save_dictionary["tick_count"])
    game_state.souls = float(save_dictionary["souls"])
    game_state.souls_multiplier = float(save_dictionary["souls_multiplier"])
    game_state.total_souls_gained = float(save_dictionary["total_souls_gained"])
    game_state.total_souls_spent = float(save_dictionary["total_souls_spent"])
    game_state.click_count = int(save_dictionary["click_count"])
    game_state.click_power = float(save_dictionary["click_power"])
    #Loading Undead
    game_state.skeleton.count = int(skeleton["count"])
    game_state.skeleton.cost = int(skeleton["cost"])
    game_state.skeleton.cost_multiplier = float(skeleton["cost_multiplier"])
    game_state.skeleton.power = float(skeleton["power"])
    game_state.zombie.count = int(zombie["count"])
    game_state.zombie.cost = int(zombie["cost"])
    game_state.zombie.cost_multiplier = float(zombie["cost_multiplier"])
    game_state.zombie.power = float(zombie["power"])
    game_state.wraith.count = int(wraith["count"])
    game_state.wraith.cost = int(wraith["cost"])
    game_state.wraith.cost_multiplier = float(wraith["cost_multiplier"])
    game_state.wraith.power = float(wraith["power"])

    upgrades_saved = save_dictionary["upgrades_status"]
    for saved in upgrades_saved:
        saved_id = int(saved)
        saved_status = upgrades_saved[saved]
        upgrade_current = game_state.upgrades[saved_id-1]
        upgrade_current["bought"] = saved_status

def save_to_json():
    save_dictionary = build_save_dictionary()
    with open("save.json", "w") as file:
        json.dump(save_dictionary, file, indent=4)



def load_from_json():
    if Path("save.json").is_file():
        try:
            with open("save.json", "r") as file:
                save_dictionary = json.load(file)
                load_save_from_dictionary(save_dictionary)
                print("Save loaded!")
        except Exception as e:
            print(f"Save loading failed: {e}")
            print("Values after failure won't load.")
            print("If you changed values in the save file, make sure to leave variable names and dictionary syntax intact!")