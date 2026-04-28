import game_state
import json
from pathlib import Path

def build_save_dictionary():
    save_dictionary = {"tick_rate": game_state.tick_rate,
                       "tick_count": game_state.tick_count,
                       "souls": game_state.souls,
                       "souls_multiplier": game_state.souls_multiplier,
                       "souls_tick_multiplier": game_state.souls_tick_multiplier,
                       "total_souls_gained": game_state.total_souls_gained,
                       "total_souls_spent": game_state.total_souls_spent,
                       "click_count": game_state.click_count,
                       "click_power": game_state.click_power,
                       "click_passive_scaling": game_state.click_passive_scaling,
                       "wraith_per_zombie_scaling": game_state.wraith_per_zombie_scaling,
                       "skeletons_per_vampire_scaling": game_state.skeletons_per_vampire_scaling,
                       "vampire_and_lich_per_wraith_scaling": game_state.vampire_and_lich_per_wraith_scaling,
                       "vampire_tick_rate": game_state.vampire_tick_rate,
                       "lich_summoning": game_state.lich_summoning,
                       "lich_summoning_wraith": game_state.lich_summoning,
                       "souls_gained_on_spend": game_state.souls_gained_on_spend,
                       "undead_king_unlocked": game_state.undead_king_unlocked,
                       "victory_achieved": game_state.victory_achieved,
                       "undeads": {},
                       "upgrades_status": {}
                       }
    # Saving Undeads
    undeads = save_dictionary["undeads"]
    for undead in game_state.undead_list:
        name = undead.name
        undeads[name] = {}
        undeads[name]["count"] = undead.count
        undeads[name]["cost"] = undead.cost
        undeads[name]["cost_multiplier"] = undead.cost_multiplier
        undeads[name]["power"] = undead.power
        undeads[name]["global_multiplier"] = undead.global_multiplier
        undeads[name]["unlocked"] = undead.unlocked
    # Saving Upgrades
    upgrades_status = save_dictionary["upgrades_status"]
    for upgrade in game_state.upgrades:
        upgrade_id = upgrade["id"]
        upgrade_bought = upgrade["bought"]
        upgrades_status[str(upgrade_id)] = upgrade_bought
    return save_dictionary

def load_save_from_dictionary(save_dictionary):
    #Loading Global Variables
    game_state.tick_rate = int(save_dictionary["tick_rate"])
    game_state.tick_count = int(save_dictionary["tick_count"])
    game_state.souls = float(save_dictionary["souls"])
    game_state.souls_multiplier = float(save_dictionary["souls_multiplier"])
    game_state.souls_tick_multiplier = float(save_dictionary["souls_tick_multiplier"])
    game_state.total_souls_gained = float(save_dictionary["total_souls_gained"])
    game_state.total_souls_spent = float(save_dictionary["total_souls_spent"])
    game_state.click_count = int(save_dictionary["click_count"])
    game_state.click_power = float(save_dictionary["click_power"])
    game_state.click_passive_scaling = float(save_dictionary["click_passive_scaling"])
    game_state.wraith_per_zombie_scaling = float(save_dictionary["wraith_per_zombie_scaling"])
    game_state.skeletons_per_vampire_scaling = float(save_dictionary["skeletons_per_vampire_scaling"])
    game_state.vampire_and_lich_per_wraith_scaling = float(save_dictionary["vampire_and_lich_per_wraith_scaling"])
    game_state.vampire_tick_rate = float(save_dictionary["vampire_tick_rate"])
    game_state.lich_summoning = int(save_dictionary["lich_summoning"])
    game_state.lich_summoning_wraith = int(save_dictionary["lich_summoning_wraith"])
    game_state.souls_gained_on_spend = float(save_dictionary["souls_gained_on_spend"])
    game_state.undead_king_unlocked = bool(save_dictionary["undead_king_unlocked"])
    game_state.victory_achieved = bool(save_dictionary["victory_achieved"])
    # Loading Undead
    undeads = save_dictionary["undeads"]
    for undead in game_state.undead_list:
        name = undead.name
        if name in undeads:
            current = undeads[name]
            undead.count = int(current["count"])
            undead.cost = int(current["cost"])
            undead.cost_multiplier = float(current["cost_multiplier"])
            undead.power = float(current["power"])
            undead.global_multiplier = float(current["global_multiplier"])
            undead.unlocked = bool(current["unlocked"])
    # Loading Upgrades
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
                return True
        except Exception as e:
            print(f"Save loading failed: {e}")
            print("Values after failure won't load.")
            print("If you changed values in the save file, make sure to leave variable names and dictionary syntax intact!")
            return False
    return False